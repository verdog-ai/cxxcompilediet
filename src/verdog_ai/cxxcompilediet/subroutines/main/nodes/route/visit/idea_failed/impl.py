from verdog_runtime.declarations import Success

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    return Success(output=input, state=state)
