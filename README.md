# cxxcompilediet

A [Verdog](https://drexlerd.github.io/verdog-website/) loop that lowers the
compile cost of C++ libraries and keeps only changes whose gain it measured.

Each round an agent (Codex) makes one change in one repository. The loop
checks the change, rebuilds that repository from scratch, runs its tests and
keeps the change as a commit only if the chosen metric dropped by at least
`threshold`:

- **Rules first.** The agent lowers the metric by applying your rules file
  (for example yggdrasil's `docs/TEMPLATE_RULES.md`) where it helps most; it
  does not have to name a rule. `apply_rules = false` skips this phase.
- **New ideas on stagnation.** After `stagnation` rounds in a row without a
  kept change, it tries an idea the rules do not cover, with its hypothesis.
- **Stop** after `max_changes` kept changes or `explore_failures` failed new
  ideas in a row.
- **Patched rules.** At the end the agent writes the rules file patched with
  what the measurements showed: new rules for kept new ideas, limits for rules
  that did not pay off, each marked "(measured: …)".

Every attempt, kept or not, goes to `attempts.jsonl`. Later runs in the same
runs directory see all earlier attempts, so a failed idea is not retried
blindly.

## Prerequisites

- Verdog: `uv tool install verdog-cli`, signed in (`verdog login`) for
  `verdog generate` and `verdog analyze`.
- [Codex](https://learn.chatgpt.com/docs/codex/cli#get-started-with-codex-cli),
  the provider of the workflow's `agent` profile.
- [plumbcheck](https://github.com/drexlerd/plumbcheck) with its Codex hooks:
  `plumbcheck hooks install --codex`. The hooks lint each edit of the agent
  in a repository that has a `plumbcheck.yml`.
- CMake, Ninja (or the generator your configure command names) and a C++
  compiler; Linux, since the measurement uses `wait4`.

## Run

```sh
verdog sync
verdog check
cp cxxcompilediet.example.toml ~/projects/cxxcompilediet.toml   # adjust
verdog run main -- --input.config ~/projects/cxxcompilediet.toml
```

Pass an absolute path. `--input.runs` names the runs directory (default
`cxxcompilediet-runs`, relative to the configuration file). Each round is at
least one clean build of one repository and one agent invocation, which uses
the provider's quota or billing.

Your checkouts are not touched: each run works in its own git worktrees on a
branch `cxxcompilediet/<run>`, with build directories under the run. Review
the branches, push what you want and remove the worktrees with
`git worktree remove`.

## Configuration

See `cxxcompilediet.example.toml`. Relative paths are relative to the file.

| Key | Meaning |
| --- | --- |
| `rules` | the rules file the agent applies and the run patches |
| `metric` | `peak_rss_mb`, `max_tu_rss_mb`, `sum_tu_seconds` or `build_seconds` |
| `threshold` | the relative drop of `metric` a change must bring to be kept |
| `max_changes` | stop after this many kept changes |
| `stagnation` | rounds without a kept change before new ideas |
| `apply_rules` | `false` starts with new ideas (default `true`) |
| `explore_failures` | stop after this many failed new ideas in a row |
| `jobs` | the build's parallelism |
| `[[repos]]` | `path`, `configure` and `test` commands; `{src}` is the run's worktree, `{build}` its build directory |

The loop adds `CMAKE_CXX_COMPILER_LAUNCHER`, `CMAKE_CXX_LINKER_LAUNCHER` and
`CMAKE_EXPORT_COMPILE_COMMANDS=ON` to each configure command.

## Metrics

CMake runs every compile and link through the launcher
`<workflow python> -m verdog_ai.cxxcompilediet.measure`, which records the
command's time and the maximum RSS of the compiler (`cc1plus`, `lto1`):

- `peak_rss_mb`: peak of the summed RSS of the commands running at the same
  time (an upper bound of the build's peak memory at `jobs`);
- `max_tu_rss_mb`: the heaviest single command;
- `sum_tu_seconds`: the summed compile and link time;
- `build_seconds`: the build's wall time.

## The graph

`main` sets the run up (worktrees, configure, baseline builds), grants the
budgets and loops: `route` sends the round to `propose` in exploit mode while
rounds without a kept change remain, else in explore mode; `measure` builds,
tests, keeps or reverts and logs the attempt; `tally` spends the budget the
round used. When no change or no new idea is left, `patch` writes the patched
rules file.

`propose` is one round's change: the agent's reply, then a check outside the
agent's sandbox. The reply must end with a JSON object
`{"repo", "idea", "hypothesis"}`; exactly one repository, the named
one, may have changed; and if that repository has a `plumbcheck.yml`, the
files changed since the run's base must be free of findings
(`plumbcheck lint`); without one the attempt records
`no plumbcheck.yml, lint skipped`. Findings go back to the agent, at most
twice; then the round is rejected and its change reverted.

Termination is certified by `verdog analyze` with three integer features:

- `changes_left` (from `max_changes`) decreases on every kept change, and
  nothing in the loop increases it;
- `rules_left` (from `stagnation`, or 0 with `apply_rules = false`)
  decreases on every failed round on the rules and is refilled only by a
  kept change;
- `ideas_left` (from `explore_failures`) decreases on every failed new idea
  and is refilled only by a kept change.

Once the kept-change arcs are removed by `changes_left`, the two refills are
gone and the remaining cycles decrease `rules_left` or `ideas_left`: a
lexicographic ranking that the analysis's repeated cycle elimination
certifies. In `propose`, `repairs_left` bounds the repairs.

## Outputs

The run directory (`<runs>/<stamp>/`) holds the worktrees, `build/`,
`build.log`, `test.log`, `<repo>.summary.json` and `<repo>.kept.jsonl` (the
kept state's measurements), `attempts.jsonl` and the patched rules file. The
workflow returns the run directory, the branch, the counts of kept changes
and attempts, and the patched rules file's path.

## Limits

- A change is measured in the changed repository only, not in the
  repositories that depend on it.
- `peak_rss_mb` counts each command with its maximum RSS for its whole run.
- plumbcheck's clang-tidy needs `build/compile_commands.json` inside the
  repository; the run's build directories are outside the worktrees, so it
  does not run in the check.

## Test without a model account

```sh
.verdog/environments/main/bin/python -m pytest -q tests
```

The tests run the whole graph with a scripted agent on a tiny CMake project:
a kept change, reverted ones, stagnation into new ideas, a repair and the
stop.

## License

AGPL-3.0-only.
