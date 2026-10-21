from typing import Final
from verdog_runtime.declarations import NodeDefinition, Agent
from verdog_ai.cxxcompilediet.subroutines.main import NODE_IDS, StateScope, PROFILE_IDS, SESSION_IDS
from .impl import Output as Output, State

NODE: Final[NodeDefinition[State, StateScope]] = NodeDefinition(id=NODE_IDS.patch, name='patch', state_type=State, operation=Agent(profile=PROFILE_IDS.agent, session=SESSION_IDS.patching))
