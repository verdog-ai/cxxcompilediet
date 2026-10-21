from typing import Final
from verdog_ai.cxxcompilediet.subroutines.propose.edges.begin__change import EDGE as BEGIN__CHANGE_EDGE
from verdog_ai.cxxcompilediet.subroutines.propose.edges.change__check import EDGE as CHANGE__CHECK_EDGE
from verdog_ai.cxxcompilediet.subroutines.propose.edges.check__verdict import EDGE as CHECK__VERDICT_EDGE
from verdog_ai.cxxcompilediet.subroutines.propose.edges.enter__begin import EDGE as ENTER__BEGIN_EDGE
from verdog_ai.cxxcompilediet.subroutines.propose.edges.repair import EDGE as REPAIR_EDGE
from verdog_ai.cxxcompilediet.subroutines.propose.edges.verdict__exit import EDGE as VERDICT__EXIT_EDGE

EDGES: Final = (BEGIN__CHANGE_EDGE, CHANGE__CHECK_EDGE, CHECK__VERDICT_EDGE, ENTER__BEGIN_EDGE, REPAIR_EDGE, VERDICT__EXIT_EDGE)
