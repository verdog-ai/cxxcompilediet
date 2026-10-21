"""Set the run up: a worktree, a configured build and a baseline per repo.

CMake runs every compile and link through the measuring launcher, this
workflow environment's Python with ``-m verdog_ai.cxxcompilediet.measure``.
"""

import shlex
import sys
from dataclasses import replace
from pathlib import Path

from verdog_runtime.declarations import Success

from verdog_ai.cxxcompilediet import diet
from verdog_ai.cxxcompilediet.diet import Diet

from . import Context, Input, Result, State


def visit_impl(input: Input, state: State, context: Context, /) -> Result:
    """Create the run directory, its worktrees and their baselines."""
    path = Path(input.config).resolve()
    config = diet.load(path)
    name = diet.stamp()
    run = (path.parent / input.runs / name).resolve()
    run.mkdir(parents=True)
    launcher = shlex.quote(
        f"{sys.executable};-m;verdog_ai.cxxcompilediet.measure"
    )
    launch = (
        f" -DCMAKE_CXX_COMPILER_LAUNCHER={launcher}"
        f" -DCMAKE_CXX_LINKER_LAUNCHER={launcher}"
        " -DCMAKE_EXPORT_COMPILE_COMMANDS=ON"
    )
    repos: list[diet.Repo] = []
    for repo in config.repos:
        base = diet.git(Path(repo.path), "rev-parse", "HEAD").strip()
        tree = run / repo.name
        diet.git(
            Path(repo.path),
            "worktree",
            "add",
            "-q",
            "-b",
            diet.BRANCH + name,
            str(tree),
            base,
        )
        repos.append(replace(repo, base=base))
    output = Diet(config=replace(config, repos=tuple(repos)), run=str(run))
    for repo in output.config.repos:
        tree, build = diet.tree(output, repo), diet.build_dir(output, repo)
        cmd = repo.configure.format(src=tree, build=build) + launch
        if not diet.sh(cmd, tree, run / "build.log"):
            raise RuntimeError(
                f"{repo.name}: configure failed, see {run}/build.log"
            )
        summary = diet.build(output, repo)
        if summary is None:
            raise RuntimeError(
                f"{repo.name}: baseline build failed, see {run}/build.log"
            )
        diet.keep(output, repo, summary)
    return Success(output=output, state=state)
