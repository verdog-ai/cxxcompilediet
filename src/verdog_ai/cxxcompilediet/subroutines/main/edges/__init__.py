from typing import Final
from verdog_ai.cxxcompilediet.subroutines.main.edges.budget__route import EDGE as BUDGET__ROUTE_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.changes_done import EDGE as CHANGES_DONE_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.enter__setup import EDGE as ENTER__SETUP_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.exploit import EDGE as EXPLOIT_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.explore import EDGE as EXPLORE_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.idea_failed import EDGE as IDEA_FAILED_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.ideas_done import EDGE as IDEAS_DONE_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.kept import EDGE as KEPT_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.measure__tally import EDGE as MEASURE__TALLY_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.patch__exit import EDGE as PATCH__EXIT_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.propose__measure import EDGE as PROPOSE__MEASURE_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.rule_failed import EDGE as RULE_FAILED_EDGE
from verdog_ai.cxxcompilediet.subroutines.main.edges.setup__budget import EDGE as SETUP__BUDGET_EDGE

EDGES: Final = (BUDGET__ROUTE_EDGE, CHANGES_DONE_EDGE, ENTER__SETUP_EDGE, EXPLOIT_EDGE, EXPLORE_EDGE, IDEA_FAILED_EDGE, IDEAS_DONE_EDGE, KEPT_EDGE, MEASURE__TALLY_EDGE, PATCH__EXIT_EDGE, PROPOSE__MEASURE_EDGE, RULE_FAILED_EDGE, SETUP__BUDGET_EDGE)
