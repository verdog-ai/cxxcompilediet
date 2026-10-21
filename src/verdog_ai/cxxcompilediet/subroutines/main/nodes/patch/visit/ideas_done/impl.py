from verdog_ai.cxxcompilediet.subroutines.main.nodes.patch.impl import patch

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    return patch(input, state, context)
