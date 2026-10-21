"""One round's change: the agent's reply, checked, repaired at most twice."""

from dataclasses import dataclass

from verdog_ai.cxxcompilediet.diet import Diet


@dataclass(frozen=True, slots=True, kw_only=True)
class Params:
    pass


Input = Diet
Output = Diet
