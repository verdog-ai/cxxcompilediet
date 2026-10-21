"""Check the reply and the change before anything is built.

The reply must name the change; exactly one repository, the named one, may
have changed; and the changed files must be free of the findings of the
repository's linters (``plumbcheck lint`` since the run's base), if the
repository has a ``plumbcheck.yml``. Findings go back to the agent while
``REPAIRS`` allows; then the round is rejected and its change reverted.
"""

import json
from dataclasses import replace
from pathlib import Path
from typing import Any, cast

from plumbcheck import linting
from verdog_runtime.declarations import Success

from verdog_ai.cxxcompilediet import diet
from verdog_ai.cxxcompilediet.diet import Proposal
from verdog_ai.cxxcompilediet.subroutines.propose.repairs import REPAIRS

from . import Context, Input, Result, State

NO_LINT = "no plumbcheck.yml, lint skipped"


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    """Record the proposal and the findings, or reject the round."""
    proposal, errors = parse(input.reply, [r.name for r in input.config.repos])
    changed = diet.changed(input)
    lint = ""
    if len(changed) != 1:
        names = ", ".join(r.name for r in changed) or "none"
        errors.append(
            f"{len(changed)} repositories changed ({names});"
            " change exactly one, and do not commit."
        )
    else:
        repo = changed[0]
        if proposal and proposal.repo != repo.name:
            errors.append(
                f"The reply names {proposal.repo}, but {repo.name} changed."
            )
        lint, findings = lint_errors(diet.tree(input, repo), repo.base)
        errors += findings
    seen = state.checks + 1
    output = replace(input, proposal=proposal, lint=lint, errors=tuple(errors))
    if errors and seen > REPAIRS:
        for repo in changed:
            diet.revert(input, repo)
        output = replace(output, errors=(), rejected="\n".join(errors))
    return Success(output=output, state=State(checks=seen))


def parse(reply: str, names: list[str]) -> tuple[Proposal | None, list[str]]:
    """The proposal of the reply's last JSON object, or what is wrong."""
    start, end = reply.rfind("{"), reply.rfind("}")
    try:
        data: object = json.loads(reply[start : end + 1])
    except json.JSONDecodeError:
        return None, ["The reply has no JSON object at its end."]
    if not isinstance(data, dict):
        return None, ["The reply's JSON is not an object."]
    fields = cast(dict[str, Any], data)
    keys = ("repo", "idea", "hypothesis")
    missing = [k for k in keys if not isinstance(fields.get(k), str)]
    if missing:
        return None, [f"The reply's JSON lacks {', '.join(missing)}."]
    if fields["repo"] not in names:
        return None, [f"repo must be one of {', '.join(names)}."]
    return Proposal(**{k: str(fields[k]) for k in keys}), []


def lint_errors(root: Path, base: str) -> tuple[str, list[str]]:
    """What linting said, and its findings in the files changed since base."""
    if not (root / "plumbcheck.yml").is_file():
        return NO_LINT, []
    findings = linting.lint_errors(root, base)
    return f"{len(findings)} findings" if findings else "clean", findings
