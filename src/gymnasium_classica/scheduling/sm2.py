"""SM-2 spaced repetition algorithm (SuperMemo 2).

Updates scheduling parameters on NodeState after each review:
easiness factor, interval, repetition count, and timestamps.

Operates independently of BKT: BKT answers *how well* the learner knows
a node, SM-2 answers *when* to review it next.
"""

from datetime import datetime

from gymnasium_classica.models.learner import NodeState, ResponseType

# SM-2 quality mapping from ResponseType
QUALITY_MAP: dict[ResponseType, int] = {
    ResponseType.CORRECT: 5,
    ResponseType.SLOW_CORRECT: 3,
    ResponseType.INCORRECT: 0,
}

# SM-2 constants
MIN_EASINESS_FACTOR = 1.3
FIRST_INTERVAL_DAYS = 1.0
SECOND_INTERVAL_DAYS = 6.0


def compute_quality(response: ResponseType) -> int:
    """Map a ResponseType to an SM-2 quality grade (0-5)."""
    return QUALITY_MAP[response]


def sm2_update(
    state: NodeState,
    response: ResponseType,
    review_time: datetime | None = None,
    spacing_multiplier: float = 1.0,
) -> NodeState:
    """Apply SM-2 algorithm to update scheduling parameters.

    Mutates *state* in-place and returns it for convenience.

    Updates: easiness_factor, repetitions, interval_days, last_review,
    last_response.

    *spacing_multiplier* (default 1.0 = unchanged) scales the fixed initial
    intervals so an experiment variant (L1-03) can widen/narrow spacing
    without forking the algorithm. It is applied to the first/second interval
    and then carried forward through the easiness progression (no
    compounding), so 1.0 reproduces the original behaviour exactly.
    """
    if review_time is None:
        review_time = datetime.now()

    quality = compute_quality(response)

    # Update easiness factor
    ef = state.easiness_factor
    ef = ef + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
    state.easiness_factor = max(MIN_EASINESS_FACTOR, ef)

    if quality >= 3:
        # Successful recall
        state.repetitions += 1
        if state.repetitions == 1:
            state.interval_days = FIRST_INTERVAL_DAYS * spacing_multiplier
        elif state.repetitions == 2:
            state.interval_days = SECOND_INTERVAL_DAYS * spacing_multiplier
        else:
            state.interval_days = state.interval_days * state.easiness_factor
    else:
        # Failed recall — reset
        state.repetitions = 0
        state.interval_days = FIRST_INTERVAL_DAYS * spacing_multiplier

    state.last_review = review_time
    state.last_response = response
    return state
