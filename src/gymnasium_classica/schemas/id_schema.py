"""ID schema for knowledge graph nodes.

Format: {TAAL}-{TYPE}-{SEGMENT}[-{SEGMENT}]...
  - 3 to 5 dash-delimited uppercase ASCII segments
  - Segment 1 (TAAL): LAT, GRC, SHA
  - Segment 2 (TYPE): G, V, C, I
  - Segments 3+: type-specific, 1-8 uppercase alphanumeric chars each

Concept/overview nodes end with -INTRO.

Examples:
  LAT-G-MORF-NOM-D1       (Latin, Grammar, Morphology, Nominative, 1st declension)
  LAT-V-F01-ESSE           (Latin, Vocabulary, Frequency band 1, esse)
  SHA-C-FIL-STOA            (Shared, Culture, Philosophy, Stoicism)
  LAT-I-VERT-PROZA-OB      (Latin, Integration, Translation, Prose, Lower school)
"""

import re

ID_PATTERN = re.compile(r"^(LAT|GRC|SHA)-(G|V|C|I)(-[A-Z0-9]{1,8}){1,4}$")

TAAL_VALUES = frozenset({"LAT", "GRC", "SHA"})
TYPE_VALUES = frozenset({"G", "V", "C", "I"})

# Valid domain prefixes per node type (segment 3)
GRAMMAR_DOMAINS = frozenset({"MORF", "SYNT", "FONL", "METR"})
VOCAB_DOMAINS = frozenset({f"F{i:02d}" for i in range(1, 16)})  # F01..F15
CULTURE_DOMAINS = frozenset({"FIL", "GES", "LIT", "MYT", "POL", "KUN", "REL"})
INTEGRATION_DOMAINS = frozenset({"VERT", "SCAN", "INTERP", "ONTL"})

DOMAIN_MAP = {
    "G": GRAMMAR_DOMAINS,
    "V": VOCAB_DOMAINS,
    "C": CULTURE_DOMAINS,
    "I": INTEGRATION_DOMAINS,
}


def validate_node_id(node_id: str) -> bool:
    """Validate that a knowledge node ID conforms to the schema."""
    return bool(ID_PATTERN.match(node_id))


def parse_node_id(node_id: str) -> dict[str, str | list[str]]:
    """Parse a knowledge node ID into its component parts.

    Returns:
        {"language": str, "type": str, "segments": list[str]}

    Raises:
        ValueError: if the ID does not match the expected pattern.
    """
    if not validate_node_id(node_id):
        raise ValueError(f"Invalid node ID: {node_id!r}")

    parts = node_id.split("-")
    return {
        "language": parts[0],
        "type": parts[1],
        "segments": parts[2:],
    }
