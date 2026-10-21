"""The check counts the replies it has seen."""

from dataclasses import dataclass

from verdog_ai.cxxcompilediet.diet import Diet


@dataclass(frozen=True, slots=True, kw_only=True)
class State:
    """How many replies of this round the check has seen."""

    checks: int = 0


Output = Diet
