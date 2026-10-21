"""Spend the budget the round used.

A kept change spends one of ``max_changes`` and refills the rounds before
new ideas and the new ideas that may fail; a failed rule application
spends a round before new ideas, a failed new idea one of the new ideas.
"""

from verdog_runtime.declarations import FeatureSuccess

from verdog_ai.cxxcompilediet import diet
from verdog_ai.cxxcompilediet.subroutines.main.features.changes_left import (
    FEATURE as CHANGES_LEFT,
)
from verdog_ai.cxxcompilediet.subroutines.main.features.ideas_left import (
    FEATURE as IDEAS_LEFT,
)
from verdog_ai.cxxcompilediet.subroutines.main.features.rules_left import (
    FEATURE as RULES_LEFT,
)

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    """Kept, failed rule or failed idea."""
    if input.kept:
        changes = state.get(CHANGES_LEFT)
        assert changes, "The route proposes only with changes left."
        return FeatureSuccess(
            state=state.replace(CHANGES_LEFT, changes - 1)
            .replace(RULES_LEFT, diet.rule_rounds(input.config))
            .replace(IDEAS_LEFT, input.config.explore_failures)
        )
    budget = IDEAS_LEFT if input.mode == "explore" else RULES_LEFT
    left = state.get(budget)
    assert left, "The route proposes only with this budget left."
    return FeatureSuccess(state=state.replace(budget, left - 1))
