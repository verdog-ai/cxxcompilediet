"""Send the check's findings back for repair."""

from dataclasses import replace
from pathlib import Path

from verdog_runtime.declarations import AgentAccess, Success

from verdog_ai.cxxcompilediet import diet

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    """Send the findings of the previous reply."""
    reply = context.invoke(
        diet.render(
            Path(__file__).with_name("prompt.md.j2"), errors=input.errors
        ),
        workspace=Path(input.run),
        access=AgentAccess.WORKSPACE_WRITE,
    )
    return Success(output=replace(input, reply=reply, errors=()), state=state)
