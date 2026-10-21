from typing import Final
from verdog_ai.cxxcompilediet.subroutines.propose import Input
from verdog_runtime.declarations import VisitDefinition, FeatureState, FeatureSuccess, NodeContext
from verdog_ai.cxxcompilediet.subroutines.propose import Params
from verdog_ai.cxxcompilediet.subroutines.propose import StateScope

State = FeatureState[StateScope]
Context = NodeContext[Params]
Result = FeatureSuccess[StateScope]

def visit(input: Input, state: State, context: Context, /) -> Result:
    from .impl import visit_impl
    return visit_impl(input, state, context)

VISIT: Final[VisitDefinition] = VisitDefinition(implementation=visit)
