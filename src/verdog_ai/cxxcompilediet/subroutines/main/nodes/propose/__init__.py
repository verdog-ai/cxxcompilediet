from typing import Final
from verdog_runtime.declarations import NodeDefinition, SubroutineCall, ParameterType
from verdog_ai.cxxcompilediet.subroutines.main import NODE_IDS, StateScope, PROFILE_IDS
from .impl import Output as Output, State
from verdog_runtime.declarations.ids import GraphId, AgentProfileId
from verdog_ai.cxxcompilediet.subroutines.propose import Input as _ChildInput, Output as _ChildOutput, Params as _ChildParams

ChildInput = _ChildInput
ChildOutput = _ChildOutput
ChildParams = _ChildParams

from verdog_ai.cxxcompilediet.subroutines.propose import Params as PROPOSE_PARAMS
from verdog_ai.cxxcompilediet.subroutines.propose import GRAPH_ID

PARAMS_TYPES: Final[dict[tuple[str, GraphId], ParameterType]] = {('.', GRAPH_ID): PROPOSE_PARAMS}
NODE: Final[NodeDefinition[State, StateScope]] = NodeDefinition(id=NODE_IDS.propose, name='propose', state_type=State, operation=SubroutineCall(definition_id=GRAPH_ID, definition_module='verdog_ai.cxxcompilediet.subroutines.propose', project_path='.', params_types=PARAMS_TYPES, profile_arguments={AgentProfileId('agent'): PROFILE_IDS.agent}, session_arguments={}))
