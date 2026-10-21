from typing import Final
from verdog_runtime.declarations import PortDefinition
from verdog_ai.cxxcompilediet.subroutines.main import NODE_IDS

PORT: Final[PortDefinition] = PortDefinition(id=NODE_IDS.failure)
