from typing import Final
from verdog_runtime.declarations import EdgeDefinition
from verdog_ai.cxxcompilediet.subroutines.propose import EDGE_IDS, NODE_IDS
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.verdict.visit.check__verdict import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.check__verdict, source=NODE_IDS.check, target=NODE_IDS.verdict, name='check to verdict', conditions=(), effects=(), visit=VISIT)
