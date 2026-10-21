from __future__ import annotations
from dataclasses import dataclass
from functools import cache
from typing import Final, Literal
from verdog_runtime.declarations.ids import EdgeId, GraphId, NodeId, FeatureId, AgentProfileId, AgentSessionId
from verdog_runtime.declarations import GraphDefinition, SubroutineDefinition
from .impl import Input, Output, Params

GRAPH_ID: Final[GraphId] = GraphId('verdog_ai.cxxcompilediet.propose')
type StateScope = Literal['verdog_ai.cxxcompilediet.propose']

@dataclass(frozen=True, slots=True, kw_only=True)
class NodeIdentifiers:
    begin: NodeId
    change: NodeId
    check: NodeId
    enter: NodeId
    exit: NodeId
    failure: NodeId
    verdict: NodeId

NODE_IDS: Final[NodeIdentifiers] = NodeIdentifiers(begin=NodeId('begin'), change=NodeId('change'), check=NodeId('check'), enter=NodeId('enter'), exit=NodeId('exit'), failure=NodeId('failure'), verdict=NodeId('verdict'))

@dataclass(frozen=True, slots=True, kw_only=True)
class EdgeIdentifiers:
    begin__change: EdgeId
    change__check: EdgeId
    check__verdict: EdgeId
    enter__begin: EdgeId
    repair: EdgeId
    verdict__exit: EdgeId

EDGE_IDS: Final[EdgeIdentifiers] = EdgeIdentifiers(begin__change=EdgeId('begin__change'), change__check=EdgeId('change__check'), check__verdict=EdgeId('check__verdict'), enter__begin=EdgeId('enter__begin'), repair=EdgeId('repair'), verdict__exit=EdgeId('verdict__exit'))

@dataclass(frozen=True, slots=True, kw_only=True)
class FeatureIdentifiers:
    repairs_left: FeatureId
    valid: FeatureId

FEATURE_IDS: Final[FeatureIdentifiers] = FeatureIdentifiers(repairs_left=FeatureId('repairs_left'), valid=FeatureId('valid'))

@dataclass(frozen=True, slots=True, kw_only=True)
class AgentProfileIdentifiers:
    agent: AgentProfileId

PROFILE_IDS: Final[AgentProfileIdentifiers] = AgentProfileIdentifiers(agent=AgentProfileId('agent'))

@dataclass(frozen=True, slots=True, kw_only=True)
class AgentSessionIdentifiers:
    conversation: AgentSessionId

SESSION_IDS: Final[AgentSessionIdentifiers] = AgentSessionIdentifiers(conversation=AgentSessionId('conversation'))

@cache
def definition() -> SubroutineDefinition[Input, Output, Params, StateScope]:
    from verdog_ai.cxxcompilediet.subroutines.propose.nodes import NODES
    from verdog_ai.cxxcompilediet.subroutines.propose.features import FEATURES
    from verdog_ai.cxxcompilediet.subroutines.propose.profiles import PROFILES, PROFILE_PARAMETERS
    from verdog_ai.cxxcompilediet.subroutines.propose.sessions import SESSIONS, SESSION_PARAMETERS
    from verdog_ai.cxxcompilediet.subroutines.propose.nodes.enter import PORT as ENTER
    from verdog_ai.cxxcompilediet.subroutines.propose.nodes.exit import PORT as EXIT
    from verdog_ai.cxxcompilediet.subroutines.propose.nodes.failure import PORT as FAILURE
    from verdog_ai.cxxcompilediet.subroutines.propose.edges import EDGES
    return SubroutineDefinition(graph=GraphDefinition[Input, Output, Params, StateScope](id=GRAPH_ID, params_type=Params, enter=ENTER, exit=EXIT, failure=FAILURE, nodes=NODES, edges=EDGES, features=FEATURES, profiles=PROFILES, profile_parameters=PROFILE_PARAMETERS, sessions=SESSIONS, session_parameters=SESSION_PARAMETERS))
