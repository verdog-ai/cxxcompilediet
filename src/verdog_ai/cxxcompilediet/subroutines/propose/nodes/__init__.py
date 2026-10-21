from typing import Final
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.begin import NODE as BEGIN_NODE
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.change import NODE as CHANGE_NODE
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.check import NODE as CHECK_NODE
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.verdict import NODE as VERDICT_NODE

NODES: Final = (BEGIN_NODE, CHANGE_NODE, CHECK_NODE, VERDICT_NODE)
