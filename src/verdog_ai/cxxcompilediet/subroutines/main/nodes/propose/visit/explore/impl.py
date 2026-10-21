"""Ask for one change in explore mode."""

from dataclasses import replace

from verdog_runtime.declarations import Success

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    output = context.invoke(replace(input, mode="explore"))
    return Success(output=output, state=state)
