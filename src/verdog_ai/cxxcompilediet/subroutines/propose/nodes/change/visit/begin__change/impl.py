"""Ask the agent for one change: a rule of the rules file, or a new idea."""

from dataclasses import replace
from pathlib import Path

from verdog_runtime.declarations import AgentAccess, Success

from verdog_ai.cxxcompilediet import diet

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    """Send the round's prompt."""
    run = Path(input.run)
    repos = [
        {
            "name": r.name,
            "tree": diet.tree(input, r),
            "build": diet.build_dir(input, r),
            "heaviest": diet.heaviest(input, r),
        }
        for r in input.config.repos
    ]
    prompt = diet.render(
        Path(__file__).with_name("prompt.md.j2"),
        config=input.config,
        mode=input.mode,
        repos=repos,
        attempts=diet.history(run.parent),
    )
    reply = context.invoke(
        prompt, workspace=run, access=AgentAccess.WORKSPACE_WRITE
    )
    return Success(output=replace(input, reply=reply, errors=()), state=state)
