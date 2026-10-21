from typing import Final
from verdog_ai.cxxcompilediet.subroutines.main.nodes.measure import Output as Input
from verdog_runtime.declarations import VisitDefinition, NodeContext, Success
from verdog_ai.cxxcompilediet.subroutines.main import Params
from verdog_ai.cxxcompilediet.subroutines.main.nodes.route import Output, State

Context = NodeContext[Params]
Result = Success[Output, State]

def visit(input: Input, state: State, context: Context, /) -> Result:
    from .impl import visit_impl
    return visit_impl(input, state, context)

VISIT: Final[VisitDefinition] = VisitDefinition(implementation=visit)
