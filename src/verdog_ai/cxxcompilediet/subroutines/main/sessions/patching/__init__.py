from typing import Final
from verdog_runtime.declarations import AgentSessionDefinition
from verdog_ai.cxxcompilediet.subroutines.main import SESSION_IDS

SESSION: Final[AgentSessionDefinition] = AgentSessionDefinition(id=SESSION_IDS.patching, name='patching', persistent=False)
