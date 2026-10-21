from typing import Final
from verdog_runtime.declarations import EdgeDefinition
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.tally.visit.measure__tally import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.measure__tally, source=NODE_IDS.measure, target=NODE_IDS.tally, name='measure to tally', conditions=(), effects=(), visit=VISIT)
