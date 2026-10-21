from __future__ import annotations
from dataclasses import dataclass
from functools import cache
from typing import Final, Literal
from verdog_runtime.declarations.ids import EdgeId, GraphId, NodeId, FeatureId, AgentProfileId, AgentSessionId
from verdog_runtime.declarations import GraphDefinition, SubroutineDefinition
from .impl import Input, Output, Params

GRAPH_ID: Final[GraphId] = GraphId('verdog_ai.cxxcompilediet.main')
type StateScope = Literal['verdog_ai.cxxcompilediet.main']

@dataclass(frozen=True, slots=True, kw_only=True)
class NodeIdentifiers:
    budget: NodeId
    enter: NodeId
    exit: NodeId
    failure: NodeId
    measure: NodeId
    patch: NodeId
    propose: NodeId
    route: NodeId
    setup: NodeId
    tally: NodeId

NODE_IDS: Final[NodeIdentifiers] = NodeIdentifiers(budget=NodeId('budget'), enter=NodeId('enter'), exit=NodeId('exit'), failure=NodeId('failure'), measure=NodeId('measure'), patch=NodeId('patch'), propose=NodeId('propose'), route=NodeId('route'), setup=NodeId('setup'), tally=NodeId('tally'))

@dataclass(frozen=True, slots=True, kw_only=True)
class EdgeIdentifiers:
    budget__route: EdgeId
    changes_done: EdgeId
    enter__setup: EdgeId
    exploit: EdgeId
    explore: EdgeId
    idea_failed: EdgeId
    ideas_done: EdgeId
    kept: EdgeId
    measure__tally: EdgeId
    patch__exit: EdgeId
    propose__measure: EdgeId
    rule_failed: EdgeId
    setup__budget: EdgeId

EDGE_IDS: Final[EdgeIdentifiers] = EdgeIdentifiers(budget__route=EdgeId('budget__route'), changes_done=EdgeId('changes_done'), enter__setup=EdgeId('enter__setup'), exploit=EdgeId('exploit'), explore=EdgeId('explore'), idea_failed=EdgeId('idea_failed'), ideas_done=EdgeId('ideas_done'), kept=EdgeId('kept'), measure__tally=EdgeId('measure__tally'), patch__exit=EdgeId('patch__exit'), propose__measure=EdgeId('propose__measure'), rule_failed=EdgeId('rule_failed'), setup__budget=EdgeId('setup__budget'))

@dataclass(frozen=True, slots=True, kw_only=True)
class FeatureIdentifiers:
    changes_left: FeatureId
    ideas_left: FeatureId
    rules_left: FeatureId

FEATURE_IDS: Final[FeatureIdentifiers] = FeatureIdentifiers(changes_left=FeatureId('changes_left'), ideas_left=FeatureId('ideas_left'), rules_left=FeatureId('rules_left'))

@dataclass(frozen=True, slots=True, kw_only=True)
class AgentProfileIdentifiers:
    agent: AgentProfileId

PROFILE_IDS: Final[AgentProfileIdentifiers] = AgentProfileIdentifiers(agent=AgentProfileId('agent'))

@dataclass(frozen=True, slots=True, kw_only=True)
class AgentSessionIdentifiers:
    patching: AgentSessionId

SESSION_IDS: Final[AgentSessionIdentifiers] = AgentSessionIdentifiers(patching=AgentSessionId('patching'))

@cache
def definition() -> SubroutineDefinition[Input, Output, Params, StateScope]:
    from verdog_ai.cxxcompilediet.subroutines.main.nodes import NODES
    from verdog_ai.cxxcompilediet.subroutines.main.features import FEATURES
    from verdog_ai.cxxcompilediet.subroutines.main.profiles import PROFILES, PROFILE_PARAMETERS
    from verdog_ai.cxxcompilediet.subroutines.main.sessions import SESSIONS, SESSION_PARAMETERS
    from verdog_ai.cxxcompilediet.subroutines.main.nodes.enter import PORT as ENTER
    from verdog_ai.cxxcompilediet.subroutines.main.nodes.exit import PORT as EXIT
    from verdog_ai.cxxcompilediet.subroutines.main.nodes.failure import PORT as FAILURE
    from verdog_ai.cxxcompilediet.subroutines.main.edges import EDGES
    return SubroutineDefinition(graph=GraphDefinition[Input, Output, Params, StateScope](id=GRAPH_ID, params_type=Params, enter=ENTER, exit=EXIT, failure=FAILURE, nodes=NODES, edges=EDGES, features=FEATURES, profiles=PROFILES, profile_parameters=PROFILE_PARAMETERS, sessions=SESSIONS, session_parameters=SESSION_PARAMETERS))
