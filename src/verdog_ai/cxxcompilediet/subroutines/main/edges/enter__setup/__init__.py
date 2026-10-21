from typing import Final
from verdog_runtime.declarations import EdgeDefinition
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.setup.visit.enter__setup import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.enter__setup, source=NODE_IDS.enter, target=NODE_IDS.setup, name='enter to setup', conditions=(), effects=(), visit=VISIT)
