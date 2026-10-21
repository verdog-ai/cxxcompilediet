"""Run the whole loop on a tiny CMake project with a scripted agent."""

import json
import subprocess
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock

import pytest
from verdog_runtime.declarations import AgentAccess, WorkflowConfiguration
from verdog_runtime.declarations.agents import AgentReply, AgentRequest
from verdog_runtime.declarations.ids import AgentProfileId, ProviderSessionId
from verdog_runtime.interpreter import Dispatcher

from verdog_ai.cxxcompilediet import diet
from verdog_ai.cxxcompilediet.subroutines.main.impl import Options, Outcome
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.check.visit.change__check import (  # noqa: E501
    impl as check,
)
from verdog_ai.cxxcompilediet.workflows.main import definition

ROOT = Path(__file__).resolve().parents[1]

HEAVY = """\
#include <cstddef>
#include <utility>

template <std::size_t I> struct S { int f() const { return int(I % 7); } };

template <std::size_t... Is> int sum(std::index_sequence<Is...>) {
  return (S<Is>{}.f() + ...);
}

int heavy() { return sum(std::make_index_sequence<4000>{}); }
"""

CMAKE = """\
cmake_minimum_required(VERSION 3.16)
project(tiny CXX)
set(CMAKE_CXX_STANDARD 17)
add_executable(tiny main.cpp heavy.cpp)
enable_testing()
add_test(NAME runs COMMAND tiny)
"""

MAIN = "int heavy();\nint main() { return heavy() < 0; }\n"


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def tiny(tmp: Path) -> Path:
    """A git repository with a heavy translation unit, and its config."""
    repo = tmp / "tiny"
    repo.mkdir()
    (repo / "CMakeLists.txt").write_text(CMAKE)
    (repo / "main.cpp").write_text(MAIN)
    (repo / "heavy.cpp").write_text(HEAVY)
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.name", "test")
    git(repo, "config", "user.email", "test@localhost")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "tiny")
    (tmp / "rules.md").write_text("1. Instantiate less.\n2. Comment.\n")
    (tmp / "cxxcompilediet.toml").write_text(
        'rules = "rules.md"\n'
        'metric = "max_tu_rss_mb"\n'
        "threshold = 0.2\n"
        "max_changes = 3\n"
        "stagnation = 1\n"
        "explore_failures = 2\n"
        "jobs = 2\n"
        "[[repos]]\n"
        'path = "tiny"\n'
        'configure = "cmake -S {src} -B {build} -G Ninja"\n'
        'test = "ctest --test-dir {build} --output-on-failure"\n'
    )
    return repo


def proposal(idea: str) -> str:
    return "Done.\n" + json.dumps(
        {"repo": "tiny", "idea": idea, "hypothesis": "less"}
    )


def comment(request: AgentRequest) -> None:
    main = request.workspace / "tiny" / "main.cpp"
    main.write_text(main.read_text() + "// no gain\n")


def lighten(request: AgentRequest) -> None:
    (request.workspace / "tiny" / "heavy.cpp").write_text(
        "int heavy() { return 1; }\n"
    )


def patch(request: AgentRequest) -> None:
    (request.workspace / "rules.md").write_text("1. (measured: kept)\n")


class Agent:
    """Replies from a script: what to change, then the reply."""

    session_provider = "test"

    def __init__(
        self, script: list[tuple[Callable[[AgentRequest], None], str]]
    ) -> None:
        self.script = script
        self.prompts: list[str] = []

    def __call__(self, request: AgentRequest, /) -> AgentReply:
        assert request.access == AgentAccess.WORKSPACE_WRITE
        self.prompts.append(request.prompt)
        act, reply = self.script.pop(0)
        act(request)
        return AgentReply(
            text=reply, provider_session_id=ProviderSessionId("round")
        )


def test_keep_revert_stagnation_explore_stop(tmp_path: Path) -> None:
    repo = tiny(tmp_path)
    head = git(repo, "rev-parse", "HEAD")
    agent = Agent(
        [
            (lighten, proposal("drop the instantiations")),
            (comment, proposal("a comment")),
            (comment, proposal("another comment")),
            (lambda _: None, "I am not sure."),
            (comment, proposal("a third comment")),
            (patch, "Written."),
        ]
    )
    workflow = replace(
        definition(),
        configuration=WorkflowConfiguration(
            profile_arguments={AgentProfileId("agent"): agent}
        ),
    )
    result = Dispatcher(project_root=ROOT).run(
        workflow,
        Options(config=str(tmp_path / "cxxcompilediet.toml")),
        output_dir=tmp_path / "out",
    )
    outcome = result.output
    assert isinstance(outcome, Outcome)
    assert agent.script == []
    run = Path(outcome.run)
    attempts = [
        json.loads(line)
        for line in (run / "attempts.jsonl").read_text().splitlines()
    ]
    assert [a["mode"] for a in attempts] == [
        "exploit",
        "exploit",
        "explore",
        "explore",
    ]
    assert [a["result"].split(",")[0] for a in attempts] == [
        "kept",
        "reverted",
        "reverted",
        "reverted",
    ]
    assert {a["lint"] for a in attempts} == {check.NO_LINT}
    assert attempts[0]["gain"] >= 0.2
    assert "applying the rules" in agent.prompts[0]
    assert "drop the instantiations -> kept" in agent.prompts[1]
    assert "Try one idea" in agent.prompts[2]
    assert "no JSON object" in agent.prompts[4]
    assert (outcome.kept, outcome.attempts) == (1, 4)
    assert Path(outcome.rules).read_text() == "1. (measured: kept)\n"
    # One commit on the run's branch; the user's checkout is untouched.
    log = git(run / "tiny", "log", "--format=%B", f"{head.strip()}..HEAD")
    assert "Mode: rules" in log and log.count("Hypothesis:") == 1
    assert git(run / "tiny", "status", "--porcelain") == ""
    assert git(repo, "rev-parse", "HEAD") == head
    assert (repo / "heavy.cpp").read_text() == HEAVY
    assert outcome.branch in git(repo, "branch", "--list", outcome.branch)


def test_lint_runs_only_with_a_plumbcheck_yml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    lint = Mock(return_value=["a.cpp:1: finding"])
    monkeypatch.setattr(check.linting, "lint_errors", lint)
    assert check.lint_errors(tmp_path, "base") == (check.NO_LINT, [])
    (tmp_path / "plumbcheck.yml").write_text("")
    assert check.lint_errors(tmp_path, "base") == (
        "1 findings",
        ["a.cpp:1: finding"],
    )
    lint.assert_called_once_with(tmp_path, "base")


def test_parse_reply() -> None:
    names = ["tiny"]
    found, errors = check.parse(proposal("x"), names)
    assert errors == [] and found and found.idea == "x"
    assert check.parse("nothing", names)[1] == [
        "The reply has no JSON object at its end."
    ]
    assert "lacks" in check.parse('{"repo": "tiny"}', names)[1][0]
    assert "one of other" in check.parse(proposal("x"), ["other"])[1][0]


def test_apply_rules_off_skips_the_rule_rounds() -> None:
    config = diet.Config(rules="r.md", repos=(), stagnation=3)
    assert diet.rule_rounds(config) == 3
    assert diet.rule_rounds(replace(config, apply_rules=False)) == 0
