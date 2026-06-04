#!/usr/bin/env python3
"""Generate audio files for vocabulary nodes in the knowledge graph.

Reads V-type nodes from data/graph/, extracts the lemma from titel_nl,
and generates an audio file per node using eSpeak NG (if available) or
a silent placeholder WAV.

Usage:
    python scripts/generate_audio.py [options]

Options:
    --graph-dir PATH   Path to graph directory (default: data/graph)
    --output-dir PATH  Path to audio output directory (default: data/audio)
    --lang {lat,grc}   Filter by language (default: both)
    --dry-run          Plan output only, do not generate files
    --force            Overwrite existing files
"""

from __future__ import annotations

import argparse
import shutil
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# ---------------------------------------------------------------------------
# Resolve project root so the script works when invoked from anywhere
# ---------------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))

from gymnasium_classica.graph.loader import load_graph
from gymnasium_classica.models.graph import NodeType

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class VocabEntry:
    """A vocabulary node ready for audio generation."""

    knoop_id: str
    lemma: str
    taal: str  # "lat" or "grc"


# ---------------------------------------------------------------------------
# Lemma extraction
# ---------------------------------------------------------------------------


def extract_lemma(titel_nl: str) -> str:
    """Extract the lemma (headword) from a titel_nl string.

    The convention is ``"lemma — translation"``.  We take everything
    before the em-dash separator.

    >>> extract_lemma("sum, esse — zijn")
    'sum, esse'
    >>> extract_lemma("εἰμί, εἶναι — zijn")
    'εἰμί, εἶναι'
    >>> extract_lemma("in (+acc/abl) — in, naar; in, op")
    'in (+acc/abl)'
    """
    if " — " in titel_nl:
        return titel_nl.split(" — ", maxsplit=1)[0].strip()
    # Fallback: return the full string stripped
    return titel_nl.strip()


# ---------------------------------------------------------------------------
# Collect vocab nodes from the graph
# ---------------------------------------------------------------------------


def collect_vocab_nodes(graph_dir: Path, lang: str | None = None) -> list[VocabEntry]:
    """Load the knowledge graph and return VocabEntry for each V-node.

    Args:
        graph_dir: Directory containing graph JSON files.
        lang: Optional filter — ``"lat"`` or ``"grc"``.  ``None`` means both.

    Returns:
        Sorted list of VocabEntry (sorted by knoop_id for determinism).
    """
    graph = load_graph(graph_dir)
    entries: list[VocabEntry] = []

    for node_id in graph.nodes:
        knoop = graph.nodes[node_id]["knoop"]
        if knoop.type != NodeType.V:
            continue
        node_lang = str(knoop.taal)
        if lang and node_lang != lang:
            continue
        lemma = extract_lemma(knoop.titel_nl)
        entries.append(VocabEntry(knoop_id=knoop.id, lemma=lemma, taal=node_lang))

    return sorted(entries, key=lambda e: e.knoop_id)


# ---------------------------------------------------------------------------
# Audio backends
# ---------------------------------------------------------------------------

_ESPEAK_LANG_MAP = {
    "lat": "la",
    "grc": "grc",
}


def _espeak_available() -> bool:
    """Return True if espeak-ng is on PATH."""
    return shutil.which("espeak-ng") is not None


def generate_espeak(entry: VocabEntry, output_path: Path) -> None:
    """Generate a WAV file using espeak-ng."""
    voice = _ESPEAK_LANG_MAP[entry.taal]
    cmd = [
        "espeak-ng",
        "-v",
        voice,
        "-s",
        "130",
        "-w",
        str(output_path),
        entry.lemma,
    ]
    subprocess.run(cmd, check=True, capture_output=True)


def generate_placeholder(output_path: Path) -> None:
    """Generate a minimal silent WAV file (0.1 s, 16-bit mono, 22050 Hz).

    This serves as a placeholder until a real TTS backend is available.
    """
    sample_rate = 22050
    num_samples = int(sample_rate * 0.1)  # 0.1 seconds
    bits_per_sample = 16
    num_channels = 1
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_size = num_samples * block_align

    with open(output_path, "wb") as f:
        # RIFF header
        f.write(b"RIFF")
        f.write(struct.pack("<I", 36 + data_size))
        f.write(b"WAVE")
        # fmt chunk
        f.write(b"fmt ")
        f.write(struct.pack("<I", 16))  # chunk size
        f.write(struct.pack("<H", 1))  # PCM format
        f.write(struct.pack("<H", num_channels))
        f.write(struct.pack("<I", sample_rate))
        f.write(struct.pack("<I", byte_rate))
        f.write(struct.pack("<H", block_align))
        f.write(struct.pack("<H", bits_per_sample))
        # data chunk
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        f.write(b"\x00" * data_size)


# ---------------------------------------------------------------------------
# Main generation loop
# ---------------------------------------------------------------------------


@dataclass
class GenerationSummary:
    """Summary of a generation run."""

    generated: int = 0
    skipped: int = 0
    errors: int = 0
    total: int = 0
    backend: str = ""
    dry_run: bool = False

    def print_report(self) -> None:
        mode = " (dry-run)" if self.dry_run else ""
        print(f"\n=== Audio Generation Summary{mode} ===")
        print(f"Backend:     {self.backend}")
        print(f"Total:       {self.total}")
        print(f"Generated:   {self.generated}")
        print(f"Skipped:     {self.skipped}")
        print(f"Errors:      {self.errors}")


def generate_all(
    entries: list[VocabEntry],
    output_dir: Path,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> GenerationSummary:
    """Generate audio for all entries.

    Args:
        entries: Vocabulary entries to process.
        output_dir: Directory to write audio files into.
        dry_run: If True, only print the plan without creating files.
        force: If True, overwrite existing files.

    Returns:
        A GenerationSummary with counts.
    """
    use_espeak = _espeak_available()
    backend_name = "espeak-ng" if use_espeak else "placeholder (silent WAV)"

    summary = GenerationSummary(
        total=len(entries),
        backend=backend_name,
        dry_run=dry_run,
    )

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)
        if not use_espeak:
            print(
                "WARNING: espeak-ng not found. Generating silent placeholder WAV files.",
                file=sys.stderr,
            )

    for entry in entries:
        ext = ".wav"
        filename = f"{entry.knoop_id}{ext}"
        filepath = output_dir / filename

        if dry_run:
            status = "PLAN"
            if filepath.exists() and not force:
                status = "SKIP (exists)"
                summary.skipped += 1
            else:
                summary.generated += 1
            print(f"  [{status}] {filename}  ←  {entry.lemma}")
            continue

        # Real generation
        if filepath.exists() and not force:
            summary.skipped += 1
            continue

        try:
            if use_espeak:
                generate_espeak(entry, filepath)
            else:
                generate_placeholder(filepath)
            summary.generated += 1
        except Exception as exc:
            print(f"  [ERROR] {filename}: {exc}", file=sys.stderr)
            summary.errors += 1

    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate audio files for vocabulary nodes.",
    )
    parser.add_argument(
        "--graph-dir",
        type=Path,
        default=_PROJECT_ROOT / "data" / "graph",
        help="Path to graph JSON directory (default: data/graph)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=_PROJECT_ROOT / "data" / "audio",
        help="Path to audio output directory (default: data/audio)",
    )
    parser.add_argument(
        "--lang",
        choices=["lat", "grc"],
        default=None,
        help="Filter by language (default: both)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan output only, do not generate files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    print(f"Loading graph from {args.graph_dir} ...")
    entries = collect_vocab_nodes(args.graph_dir, lang=args.lang)
    print(f"Found {len(entries)} vocabulary nodes.")

    if not entries:
        print("Nothing to generate.")
        return 0

    summary = generate_all(
        entries,
        args.output_dir,
        dry_run=args.dry_run,
        force=args.force,
    )
    summary.print_report()

    return 1 if summary.errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
