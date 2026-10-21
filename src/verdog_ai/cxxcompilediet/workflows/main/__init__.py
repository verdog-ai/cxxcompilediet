from __future__ import annotations
from dataclasses import dataclass
from functools import cache
from typing import Final
from .bindings import CONFIGURATION
from .sessions import SESSIONS
from verdog_runtime.declarations import ParameterType, SubroutineCall, WorkflowConfiguration, WorkflowDefinition
from verdog_runtime.declarations.ids import GraphId, AgentProfileId
from verdog_ai.cxxcompilediet.subroutines.main import GRAPH_ID as ENTRY_GRAPH_ID, Input, Output, Params, StateScope
from verdog_ai.cxxcompilediet.subroutines.propose import Params as PROPOSE_PARAMS
from verdog_ai.cxxcompilediet.subroutines.propose import GRAPH_ID as PROPOSE_GRAPH_ID

PARAMS_TYPES: Final[dict[tuple[str, GraphId], ParameterType]] = {('.', ENTRY_GRAPH_ID): Params, ('.', PROPOSE_GRAPH_ID): PROPOSE_PARAMS}

@dataclass(frozen=True, slots=True, kw_only=True)
class RuntimeOptions:
    pass

def configure(options: RuntimeOptions, /) -> WorkflowConfiguration:
    return CONFIGURATION

GRAPH_ID: Final[GraphId] = GraphId('verdog_ai.cxxcompilediet.main')
ENTRY: Final[SubroutineCall] = SubroutineCall(definition_id=ENTRY_GRAPH_ID, definition_module='verdog_ai.cxxcompilediet.subroutines.main', project_path='.', params_types=PARAMS_TYPES, profile_arguments={AgentProfileId('agent'): AgentProfileId('agent')}, session_arguments={})

@cache
def definition() -> WorkflowDefinition[Input, Output, Params, StateScope]:
    return WorkflowDefinition(id=GRAPH_ID, input_type=Input, entry=ENTRY, sessions=SESSIONS, configuration=CONFIGURATION)
