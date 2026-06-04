#!/usr/bin/env python3
"""Report content coverage per node and aggregate per (taal, type).

For every node in the knowledge graph this script checks four coverage
dimensions:

* ``has_items`` — the node has at least one Item attached.
* ``has_content`` — a markdown file ``data/content/{id}.md`` exists OR the
  node's ``content_ref`` points to an existing file.
* ``has_audio`` — only for V-nodes: ``data/audio/{id}.wav`` exists and is
  larger than 1 KB.
* ``in_passage`` — the node ID occurs in the ``knoop_ids`` list of any
  passage in ``data/passages/*.json``.

Usage::

    python scripts/content_coverage.py
    python scripts/content_coverage.py --output data/content_coverage.json

Run the aggregate numbers through the pytest-regressiecheck in
``tests/test_content_coverage.py`` to prevent regressions on CI.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

import networkx as nx

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.graph import Language, Node, NodeType

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GRAPH_DIR = REPO_ROOT / "data" / "graph"
DEFAULT_CONTENT_DIR = REPO_ROOT / "data" / "content"
DEFAULT_AUDIO_DIR = REPO_ROOT / "data" / "audio"
DEFAULT_PASSAGES_DIR = REPO_ROOT / "data" / "passages"

AUDIO_MIN_BYTES = 1024


@dataclass
class KnoopCoverage:
    """Coverage flags for a single node."""

    id: str
    taal: str
    type: str
    has_items: bool
    has_content: bool
    has_audio: bool
    in_passage: bool


@dataclass
class CoverageSummary:
    """Aggregate coverage counts + percentages for a (taal, type) bucket."""

    taal: str
    type: str
    total: int
    items: int
    content: int
    audio: int
    passage: int
    items_pct: float
    content_pct: float
    audio_pct: float
    passage_pct: float


@dataclass
class CoverageReport:
    """Full coverage report: per-node records + per-bucket summaries."""

    knopen: list[KnoopCoverage] = field(default_factory=list)
    summaries: list[CoverageSummary] = field(default_factory=list)


def _collect_passage_node_ids(passages_dir: Path) -> set[str]:
    """Gather every node_id referenced by any passage JSON."""
    ids: set[str] = set()
    if not passages_dir.exists():
        return ids
    for path in sorted(passages_dir.glob("*.json")):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for passage in data.get("passages", []):
            for kid in passage.get("knoop_ids", []):
                ids.add(kid)
    return ids


def _content_exists(node: Node, content_dir: Path) -> bool:
    """Resolve either `{id}.md` or `content_ref` against the content directory."""
    if (content_dir / f"{node.id}.md").exists():
        return True
    if node.content_ref:
        ref = Path(node.content_ref)
        # content_ref may be relative ('data/content/foo.md') or bare ('foo.md')
        candidates = [
            REPO_ROOT / ref,
            content_dir / ref.name,
        ]
        return any(c.exists() for c in candidates)
    return False


def _audio_ok(node: Node, audio_dir: Path) -> bool:
    """V-nodes only: the audio file must exist AND be > 1 KB."""
    if node.type != NodeType.V:
        return False
    path = audio_dir / f"{node.id}.wav"
    return path.exists() and path.stat().st_size > AUDIO_MIN_BYTES


def _safe_pct(part: int, total: int) -> float:
    return round(100.0 * part / total, 2) if total else 0.0


def compute_coverage(
    graph: nx.DiGraph,
    *,
    content_dir: Path = DEFAULT_CONTENT_DIR,
    audio_dir: Path = DEFAULT_AUDIO_DIR,
    passages_dir: Path = DEFAULT_PASSAGES_DIR,
) -> CoverageReport:
    """Walk the graph and produce per-node and per-bucket coverage data."""
    passage_ids = _collect_passage_node_ids(passages_dir)

    report = CoverageReport()
    # (taal, type) -> counters
    buckets: dict[tuple[str, str], dict[str, int]] = {}

    for node_id in graph.nodes:
        node: Node = graph.nodes[node_id]["node"]
        has_items = len(node.items) > 0
        has_content = _content_exists(node, content_dir)
        has_audio = _audio_ok(node, audio_dir)
        in_passage = node.id in passage_ids

        report.knopen.append(
            KnoopCoverage(
                id=node.id,
                taal=node.taal.value,
                type=node.type.value,
                has_items=has_items,
                has_content=has_content,
                has_audio=has_audio,
                in_passage=in_passage,
            )
        )

        key = (node.taal.value, node.type.value)
        bucket = buckets.setdefault(
            key,
            {"total": 0, "items": 0, "content": 0, "audio": 0, "passage": 0},
        )
        bucket["total"] += 1
        if has_items:
            bucket["items"] += 1
        if has_content:
            bucket["content"] += 1
        if has_audio:
            bucket["audio"] += 1
        if in_passage:
            bucket["passage"] += 1

    for (taal, ktype), counts in sorted(buckets.items()):
        total = counts["total"]
        report.summaries.append(
            CoverageSummary(
                taal=taal,
                type=ktype,
                total=total,
                items=counts["items"],
                content=counts["content"],
                audio=counts["audio"],
                passage=counts["passage"],
                items_pct=_safe_pct(counts["items"], total),
                content_pct=_safe_pct(counts["content"], total),
                audio_pct=_safe_pct(counts["audio"], total),
                passage_pct=_safe_pct(counts["passage"], total),
            )
        )

    report.knopen.sort(key=lambda k: k.id)
    return report


def find_summary(
    report: CoverageReport, taal: Language | str, ktype: NodeType | str
) -> CoverageSummary | None:
    """Look up the summary for a (taal, type) bucket; None if absent."""
    taal_v = taal.value if isinstance(taal, Language) else taal
    type_v = ktype.value if isinstance(ktype, NodeType) else ktype
    for s in report.summaries:
        if s.taal == taal_v and s.type == type_v:
            return s
    return None


def report_to_dict(report: CoverageReport) -> dict:
    """JSON-serialisable view of the report."""
    return {
        "knopen": [asdict(k) for k in report.knopen],
        "summaries": [asdict(s) for s in report.summaries],
    }


def _format_summary_table(report: CoverageReport) -> str:
    header = (
        f"{'taal':<6} {'type':<4} {'total':>5}  "
        f"{'items':>16} {'content':>16} {'audio':>16} {'passage':>16}"
    )
    lines = [header, "-" * len(header)]
    for s in report.summaries:
        items_cell = f"{s.items}/{s.total} ({s.items_pct:.1f}%)"
        content_cell = f"{s.content}/{s.total} ({s.content_pct:.1f}%)"
        audio_cell = f"{s.audio}/{s.total} ({s.audio_pct:.1f}%)" if s.type == "V" else "n.v.t."
        passage_cell = f"{s.passage}/{s.total} ({s.passage_pct:.1f}%)"
        lines.append(
            f"{s.taal:<6} {s.type:<4} {s.total:>5}  "
            f"{items_cell:>16} {content_cell:>16} {audio_cell:>16} {passage_cell:>16}"
        )
    return "\n".join(lines)


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rapporteer content-dekking per node en per (taal, type).",
    )
    parser.add_argument(
        "--graph-dir",
        type=Path,
        default=DEFAULT_GRAPH_DIR,
        help="Map met graph-JSON-bestanden (default: data/graph).",
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=DEFAULT_CONTENT_DIR,
        help="Map met markdown-content (default: data/content).",
    )
    parser.add_argument(
        "--audio-dir",
        type=Path,
        default=DEFAULT_AUDIO_DIR,
        help="Map met audio-bestanden (default: data/audio).",
    )
    parser.add_argument(
        "--passages-dir",
        type=Path,
        default=DEFAULT_PASSAGES_DIR,
        help="Map met passage-JSON-bestanden (default: data/passages).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optioneel: schrijf het volledige rapport als JSON naar dit pad.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    graph = load_graph(args.graph_dir)
    report = compute_coverage(
        graph,
        content_dir=args.content_dir,
        audio_dir=args.audio_dir,
        passages_dir=args.passages_dir,
    )

    print(f"=== Content-dekking ({graph.number_of_nodes()} knopen) ===")
    print(_format_summary_table(report))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(report_to_dict(report), f, ensure_ascii=False, indent=2)
        print(f"\nJSON-rapport geschreven naar {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
