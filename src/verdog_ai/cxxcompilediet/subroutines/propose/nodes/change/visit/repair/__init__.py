from typing import Final
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.check import Output as Input
from verdog_runtime.declarations import VisitDefinition, AgentNodeContext, Success
from verdog_ai.cxxcompilediet.subroutines.propose import Params
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.change import Output, State

Context = AgentNodeContext[Params]
Result = Success[Output, State]

def visit(input: Input, state: State, context: Context, /) -> Result:
    from .impl import visit_impl
    return visit_impl(input, state, context)

VISIT: Final[VisitDefinition] = VisitDefinition(implementation=visit)
