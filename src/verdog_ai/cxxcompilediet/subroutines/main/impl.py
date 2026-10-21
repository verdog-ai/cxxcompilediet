"""The loop's boundary: a configuration file in, the run's outcome out."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class Options:
    """The configuration file and the directory of the runs.

    A relative ``runs`` is relative to the configuration file.
    """

    config: str = "cxxcompilediet.toml"
    runs: str = "cxxcompilediet-runs"


@dataclass(frozen=True, slots=True, kw_only=True)
class Outcome:
    """Where the run is, what it kept and the patched rules file."""

    run: str
    branch: str
    kept: int
    attempts: int
    rules: str


@dataclass(frozen=True, slots=True, kw_only=True)
class Params:
    pass


Input = Options
Output = Outcome
