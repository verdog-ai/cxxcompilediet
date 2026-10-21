from typing import Final
from verdog_ai.cxxcompilediet.subroutines.main.nodes.route import Output as Input
from verdog_runtime.declarations import CallContext, CallVisitDefinition, Success
from verdog_ai.cxxcompilediet.subroutines.main import Params
from verdog_ai.cxxcompilediet.subroutines.main.nodes.propose import Output, State
from verdog_ai.cxxcompilediet.subroutines.main.nodes.propose import ChildInput, ChildOutput, ChildParams

Context = CallContext[Params, ChildParams, ChildInput, ChildOutput]
Result = Success[Output, State]

def visit(input: Input, state: State, context: Context, /) -> Result:
    from .impl import visit_impl
    return visit_impl(input, state, context)

VISIT: Final[CallVisitDefinition[Input, Output, State, Params, ChildInput, ChildOutput, ChildParams]] = CallVisitDefinition(implementation=visit)
