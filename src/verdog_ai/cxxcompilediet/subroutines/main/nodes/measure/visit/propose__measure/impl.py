"""Measure the round's change: keep it as a commit if it pays off.

The changed repository is rebuilt from scratch and tested. The change is
committed, with its numbers, rule and hypothesis, if the metric dropped by
at least ``threshold``, and reverted otherwise. Every round, kept or not,
is a line of ``attempts.jsonl``.
"""

import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from verdog_runtime.declarations import Success

from verdog_ai.cxxcompilediet import diet, measure
from verdog_ai.cxxcompilediet.diet import Diet, Proposal, Repo

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    """Judge the change and log the attempt."""
    entry: dict[str, Any] = {"round": input.round + 1, "mode": input.mode}
    if input.proposal:
        entry |= asdict(input.proposal)
    entry["lint"] = input.lint
    kept = False
    if input.rejected or not input.proposal:
        entry["result"] = f"rejected: {input.rejected}"
    else:
        repo = diet.repo_named(input, input.proposal.repo)
        kept = judge(input, repo, input.proposal, entry)
    run = Path(input.run)
    with (run / diet.ATTEMPTS).open("a") as log:
        log.write(json.dumps(entry) + "\n")
    output = replace(
        input,
        round=input.round + 1,
        reply="",
        errors=(),
        proposal=None,
        lint="",
        rejected="",
        kept=kept,
    )
    return Success(output=output, state=state)


def judge(
    input: Diet, repo: Repo, proposal: Proposal, entry: dict[str, Any]
) -> bool:
    """Build, test and compare; commit the change if it pays off."""
    metric = input.config.metric
    old = measure.value(diet.kept_summary(input, repo), metric)
    summary = diet.build(input, repo)
    tested = summary is not None and diet.sh(
        repo.test.format(
            src=diet.tree(input, repo), build=diet.build_dir(input, repo)
        ),
        diet.tree(input, repo),
        Path(input.run) / "test.log",
    )
    if summary is None or not tested:
        diet.revert(input, repo)
        entry["result"] = "build failed" if summary is None else "tests failed"
        return False
    new = measure.value(summary, metric)
    gain = diet.gain(old, new)
    entry |= {"before": old, "after": new, "gain": gain}
    numbers = f"{metric} {old:.1f} -> {new:.1f} ({-gain:+.1%})"
    if gain < input.config.threshold:
        diet.revert(input, repo)
        entry["result"] = f"reverted, {numbers}"
        return False
    tree = diet.tree(input, repo)
    diet.git(tree, "add", "-A")
    diet.git(
        tree,
        "commit",
        "-q",
        "-m",
        f"{proposal.idea}\n\n{numbers}\n"
        f"Rule: {proposal.rule}\nHypothesis: {proposal.hypothesis}",
    )
    diet.keep(input, repo, summary)
    entry["result"] = f"kept, {numbers}"
    return True
