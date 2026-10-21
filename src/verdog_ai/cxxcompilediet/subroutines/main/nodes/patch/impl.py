"""The agent writes the rules file patched with what the runs measured."""

import json
from dataclasses import dataclass
from pathlib import Path

from verdog_runtime.declarations import AgentAccess, AgentNodeContext, Success

from verdog_ai.cxxcompilediet import diet
from verdog_ai.cxxcompilediet.diet import Diet
from verdog_ai.cxxcompilediet.subroutines.main.impl import Outcome, Params


@dataclass(frozen=True, slots=True, kw_only=True)
class State:
    pass


Output = Outcome


def patch(
    input: Diet, state: State, context: AgentNodeContext[Params]
) -> Success[Output, State]:
    """Ask for the patched rules file in the run directory; the outcome."""
    run = Path(input.run)
    out = run / Path(input.config.rules).name
    context.invoke(
        diet.render(
            Path(__file__).with_name("prompts") / "patch.md.j2",
            config=input.config,
            out=out,
            history=json.dumps(diet.history(run.parent), indent=1),
        ),
        workspace=run,
        access=AgentAccess.WORKSPACE_WRITE,
    )
    current = diet.attempts(run)
    outcome = Outcome(
        run=str(run),
        branch=diet.BRANCH + run.name,
        kept=sum(a["result"].startswith("kept") for a in current),
        attempts=len(current),
        rules=str(out) if out.is_file() else "",
    )
    return Success(output=outcome, state=state)
