from typing import Final
from verdog_runtime.declarations import EdgeDefinition
from verdog_ai.cxxcompilediet.subroutines.propose import EDGE_IDS, NODE_IDS
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.check.visit.change__check import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.change__check, source=NODE_IDS.change, target=NODE_IDS.check, name='change to check', conditions=(), effects=(), visit=VISIT)
