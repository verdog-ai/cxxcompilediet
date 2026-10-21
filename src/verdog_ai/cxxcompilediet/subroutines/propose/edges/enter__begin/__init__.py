from typing import Final
from verdog_runtime.declarations import EdgeDefinition
from verdog_ai.cxxcompilediet.subroutines.propose import EDGE_IDS, NODE_IDS
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.begin.visit.enter__begin import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.enter__begin, source=NODE_IDS.enter, target=NODE_IDS.begin, name='enter to begin', conditions=(), effects=(), visit=VISIT)
