from typing import Final
from verdog_runtime.declarations import EdgeDefinition
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.budget.visit.setup__budget import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.setup__budget, source=NODE_IDS.setup, target=NODE_IDS.budget, name='setup to budget', conditions=(), effects=(), visit=VISIT)
