"""Accept the reply, or spend a repair."""

from verdog_runtime.declarations import FeatureSuccess

from verdog_ai.cxxcompilediet.subroutines.propose.features.repairs_left import (
    FEATURE as REPAIRS_LEFT,
)
from verdog_ai.cxxcompilediet.subroutines.propose.features.valid import (
    FEATURE as VALID,
)

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    """The check turns findings after the last repair into a rejection."""
    if not input.errors:
        return FeatureSuccess(state=state.replace(VALID, True))
    left = state.get(REPAIRS_LEFT)
    assert left, "The check rejects once no repair remains."
    return FeatureSuccess(
        state=state.replace(VALID, False).replace(REPAIRS_LEFT, left - 1)
    )
