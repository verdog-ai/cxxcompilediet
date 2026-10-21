"""Grant the run its budgets from the configuration."""

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
    """``max_changes``, ``stagnation`` (0 without rules) and ``explore_failures``."""
    config = input.config
    return FeatureSuccess(
        state=state.replace(CHANGES_LEFT, config.max_changes)
        .replace(RULES_LEFT, diet.rule_rounds(config))
        .replace(IDEAS_LEFT, config.explore_failures)
    )
