from typing import Final
from verdog_ai.cxxcompilediet.subroutines.main.nodes.budget import NODE as BUDGET_NODE
from verdog_ai.cxxcompilediet.subroutines.main.nodes.measure import NODE as MEASURE_NODE
from verdog_ai.cxxcompilediet.subroutines.main.nodes.patch import NODE as PATCH_NODE
from verdog_ai.cxxcompilediet.subroutines.main.nodes.propose import NODE as PROPOSE_NODE
from verdog_ai.cxxcompilediet.subroutines.main.nodes.route import NODE as ROUTE_NODE
from verdog_ai.cxxcompilediet.subroutines.main.nodes.setup import NODE as SETUP_NODE
from verdog_ai.cxxcompilediet.subroutines.main.nodes.tally import NODE as TALLY_NODE

NODES: Final = (BUDGET_NODE, MEASURE_NODE, PATCH_NODE, PROPOSE_NODE, ROUTE_NODE, SETUP_NODE, TALLY_NODE)
