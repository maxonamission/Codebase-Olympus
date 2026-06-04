"""Non-interference scheduling for vocabulary items.

When selecting successive vocabulary items, items from the same semantic
cluster receive a negative priority modifier so they are spread apart.
This prevents interference between conceptually related words
(e.g. pater/mater, gladius/scutum) which hurts recall when practised
back-to-back (Interleaving effect, Rohrer & Taylor 2007).

The constraint is implemented as a *soft penalty*, not a hard filter:
a recently-seen cluster reduces priority but does not block selection
entirely.  This allows the scheduler to still pick a same-cluster item
when it is genuinely urgent (e.g. about to be forgotten).
"""

from dataclasses import dataclass, field

from gymnasium_classica.models.graph import KnoopType, Node


@dataclass
class NonInterferenceState:
    """Tracks recently selected clusters to compute penalties.

    *window_size* controls how many recent selections are penalised.
    *penalty_weights* maps recency position (0 = most recent) to the
    penalty factor applied.  Default: the item selected 1 step ago gets
    a 0.8 penalty, 2 steps ago 0.5, 3 steps ago 0.2.
    """

    window_size: int = 3
    penalty_weights: list[float] = field(default_factory=lambda: [0.8, 0.5, 0.2])
    _recent_clusters: list[str | None] = field(default_factory=list)
    _cluster_counts: dict[str, int] = field(default_factory=dict)
    _total_selections: int = 0

    def record_selection(self, knoop: Node) -> None:
        """Record that *knoop* was just selected."""
        cluster = knoop.semantisch_cluster if knoop.type == KnoopType.V else None
        self._recent_clusters.append(cluster)
        if len(self._recent_clusters) > self.window_size:
            self._recent_clusters = self._recent_clusters[-self.window_size :]
        self._total_selections += 1
        if cluster is not None:
            self._cluster_counts[cluster] = self._cluster_counts.get(cluster, 0) + 1

    def cluster_penalty(self, knoop: Node) -> float:
        """Return a penalty in [0.0, 1.0] for selecting *knoop* next.

        Returns 0.0 (no penalty) when the node is not a vocabulary node,
        has no cluster, or its cluster was not recently seen.

        Returns a positive value up to the largest single penalty weight
        when the cluster matches a recently selected item.  Only the
        *strongest* match counts (not cumulative), since the goal is to
        spread items apart, not to permanently suppress a cluster.
        """
        if knoop.type != KnoopType.V or knoop.semantisch_cluster is None:
            return 0.0

        cluster = knoop.semantisch_cluster
        max_penalty = 0.0

        # Walk backwards through recent selections
        for i, recent in enumerate(reversed(self._recent_clusters)):
            if i >= len(self.penalty_weights):
                break
            if recent == cluster:
                max_penalty = max(max_penalty, self.penalty_weights[i])

        return max_penalty

    def apply_penalty(self, base_priority: float, knoop: Node) -> float:
        """Return the adjusted priority after applying the cluster penalty.

        ``adjusted = base_priority * (1 - penalty)``

        A penalty of 0.8 reduces priority to 20% of its base value.
        A penalty of 0.0 leaves it unchanged.
        """
        penalty = self.cluster_penalty(knoop)
        return base_priority * (1.0 - penalty)

    @property
    def recent_clusters(self) -> list[str | None]:
        """The recent cluster history (most recent last)."""
        return list(self._recent_clusters)


def select_next(
    candidates: list[tuple[float, Node]],
    state: NonInterferenceState,
) -> Node | None:
    """Select the best candidate after applying non-interference penalties.

    *candidates* is a list of ``(base_priority, knoop)`` pairs, where
    higher priority = more desirable.

    When adjusted priorities are tied, the candidate whose cluster has been
    selected least often is preferred (fairness tiebreaker).  This ensures
    even distribution across clusters when base priorities are equal.

    Returns the selected Node (and updates *state*), or None if
    *candidates* is empty.
    """
    if not candidates:
        return None

    best_knoop = None
    best_score: tuple[float, float] = (-float("inf"), -float("inf"))

    for base_priority, knoop in candidates:
        adjusted = state.apply_penalty(base_priority, knoop)
        # Tiebreaker: prefer clusters selected fewer times (negative count → higher)
        cluster = knoop.semantisch_cluster
        count = state._cluster_counts.get(cluster, 0) if cluster else 0
        score = (adjusted, -count)
        if score > best_score:
            best_score = score
            best_knoop = knoop

    if best_knoop is None:
        return None
    state.record_selection(best_knoop)
    return best_knoop
