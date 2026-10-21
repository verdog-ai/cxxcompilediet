"""Grant a fixed number of repairs."""

from verdog_runtime.declarations import FeatureSuccess

from verdog_ai.cxxcompilediet.subroutines.propose.features.repairs_left import (
    FEATURE as REPAIRS_LEFT,
)
from verdog_ai.cxxcompilediet.subroutines.propose.repairs import REPAIRS

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    """Grant ``REPAIRS`` repairs."""
    return FeatureSuccess(state=state.replace(REPAIRS_LEFT, REPAIRS))
