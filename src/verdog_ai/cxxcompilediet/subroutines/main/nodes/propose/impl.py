from dataclasses import dataclass

from verdog_ai.cxxcompilediet.diet import Diet


@dataclass(frozen=True, slots=True, kw_only=True)
class State:
    pass


Output = Diet
