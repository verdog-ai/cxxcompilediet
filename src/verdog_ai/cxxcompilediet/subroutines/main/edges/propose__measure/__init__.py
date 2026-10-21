from typing import Final
from verdog_runtime.declarations import EdgeDefinition
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.measure.visit.propose__measure import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.propose__measure, source=NODE_IDS.propose, target=NODE_IDS.measure, name='propose to measure', conditions=(), effects=(), visit=VISIT)
