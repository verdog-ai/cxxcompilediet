"""The run's configuration, its payload and the steps the nodes share.

A run lives in its own directory under the runs directory: one git worktree
per repository on the branch ``cxxcompilediet/<run>``, its build directory
under ``build/``, the measurements of the kept state of each repository and
``attempts.jsonl``, one line per round.
"""

import json
import shutil
import subprocess
import time
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jinja2 import StrictUndefined, Template

from verdog_ai.cxxcompilediet import measure

BRANCH = "cxxcompilediet/"
ATTEMPTS = "attempts.jsonl"
HEAVIEST = 15


@dataclass(frozen=True, slots=True, kw_only=True)
class Repo:
    """A repository under the loop; ``base`` is where its run branch starts."""

    name: str
    path: str
    configure: str
    test: str
    base: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class Config:
    """``cxxcompilediet.toml``; relative paths are relative to the file."""

    rules: str
    repos: tuple[Repo, ...]
    metric: str = "peak_rss_mb"
    threshold: float = 0.02
    max_changes: int = 10
    stagnation: int = 3
    apply_rules: bool = True
    explore_failures: int = 3
    jobs: int = 16


@dataclass(frozen=True, slots=True, kw_only=True)
class Proposal:
    """What the agent says it changed, and why."""

    repo: str
    idea: str
    hypothesis: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Diet:
    """The payload of the loop: the run and its current round."""

    config: Config
    run: str
    round: int = 0
    mode: str = "exploit"
    reply: str = ""
    errors: tuple[str, ...] = ()
    proposal: Proposal | None = None
    lint: str = ""
    rejected: str = ""
    kept: bool = False


def rule_rounds(config: Config) -> int:
    """Failed rounds allowed on the rules before new ideas; 0 skips them."""
    return config.stagnation if config.apply_rules else 0


def load(path: Path) -> Config:
    """Read and check the configuration file."""
    raw: dict[str, Any] = tomllib.loads(path.read_text())
    base = path.parent
    repos = tuple(
        Repo(
            name=(base / r["path"]).resolve().name,
            path=str((base / r["path"]).resolve()),
            configure=r["configure"],
            test=r["test"],
        )
        for r in raw.pop("repos")
    )
    rules = str((base / raw.pop("rules")).resolve())
    config = Config(rules=rules, repos=repos, **raw)
    if config.metric not in measure.METRICS:
        raise ValueError(f"metric must be one of {', '.join(measure.METRICS)}")
    counts = (config.max_changes, config.stagnation, config.explore_failures)
    if min(counts) < 0 or config.jobs < 1:
        raise ValueError(
            "max_changes, stagnation, explore_failures >= 0, jobs >= 1"
        )
    if len({r.name for r in repos}) != len(repos):
        raise ValueError("repository folder names must differ")
    return config


def stamp() -> str:
    """A run's name: the time it starts."""
    return time.strftime("%Y%m%d-%H%M%S")


def tree(diet: Diet, repo: Repo) -> Path:
    """The run's worktree of ``repo``."""
    return Path(diet.run) / repo.name


def build_dir(diet: Diet, repo: Repo) -> Path:
    """The run's build directory of ``repo``."""
    return Path(diet.run) / "build" / repo.name


def git(root: Path, *args: str) -> str:
    """Run git in ``root`` and return its output."""
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def sh(cmd: str, cwd: Path, log: Path) -> bool:
    """Run a shell command with its output appended to ``log``."""
    with log.open("a") as out:
        return (
            subprocess.run(
                cmd, shell=True, cwd=cwd, stdout=out, stderr=out
            ).returncode
            == 0
        )


def build(diet: Diet, repo: Repo) -> measure.Summary | None:
    """Build ``repo`` from scratch; its summary, or None if it fails."""
    run = Path(diet.run)
    log = run / f"{repo.name}.records.jsonl"
    log.unlink(missing_ok=True)
    start = time.time()
    ok = sh(
        f"CXXCOMPILEDIET_LOG={log} cmake --build {build_dir(diet, repo)}"
        f" -j{diet.config.jobs} --clean-first",
        tree(diet, repo),
        run / "build.log",
    )
    if not ok:
        return None
    return measure.summarize(measure.read(log), time.time() - start)


def keep(diet: Diet, repo: Repo, summary: measure.Summary) -> None:
    """Record the last build of ``repo`` as its kept state."""
    run = Path(diet.run)
    shutil.copy(
        run / f"{repo.name}.records.jsonl", run / f"{repo.name}.kept.jsonl"
    )
    (run / f"{repo.name}.summary.json").write_text(json.dumps(summary))


def kept_summary(diet: Diet, repo: Repo) -> measure.Summary:
    """The summary of the kept state of ``repo``."""
    path = Path(diet.run) / f"{repo.name}.summary.json"
    return measure.Summary(**json.loads(path.read_text()))


def heaviest(diet: Diet, repo: Repo) -> list[measure.Record]:
    """The heaviest commands of the kept state of ``repo``, by RSS."""
    records = measure.read(Path(diet.run) / f"{repo.name}.kept.jsonl")
    return sorted(records, key=lambda r: -r["rss_mb"])[:HEAVIEST]


def changed(diet: Diet) -> list[Repo]:
    """The repositories with uncommitted changes in the run."""
    return [
        r
        for r in diet.config.repos
        if git(tree(diet, r), "status", "--porcelain")
    ]


def revert(diet: Diet, repo: Repo) -> None:
    """Drop the uncommitted change of ``repo``."""
    git(tree(diet, repo), "reset", "-q", "--hard")
    git(tree(diet, repo), "clean", "-fdq")


def repo_named(diet: Diet, name: str) -> Repo:
    """The repository ``name`` of the run."""
    return next(r for r in diet.config.repos if r.name == name)


def gain(old: float, new: float) -> float:
    """The relative drop from ``old`` to ``new``; negative is worse."""
    return (old - new) / old if old else 0.0


def attempts(run: Path) -> list[dict[str, Any]]:
    """The attempts of the run ``run``."""
    log = run / ATTEMPTS
    lines = log.read_text().splitlines() if log.is_file() else []
    return [json.loads(line) for line in lines]


def history(runs: Path) -> list[dict[str, Any]]:
    """The attempts of every run under ``runs``."""
    return [
        a
        for log in sorted(runs.glob(f"*/{ATTEMPTS}"))
        for a in attempts(log.parent)
    ]


def render(template: Path, **values: object) -> str:
    """Render the prompt ``template`` with ``values``."""
    return Template(
        template.read_text(encoding="utf-8"),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    ).render(**values)
