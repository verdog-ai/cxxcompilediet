from typing import Final
from verdog_runtime.declarations import NodeDefinition, Python
from verdog_ai.cxxcompilediet.subroutines.main import NODE_IDS, StateScope
from .impl import Output as Output, State

NODE: Final[NodeDefinition[State, StateScope]] = NodeDefinition(id=NODE_IDS.setup, name='setup', state_type=State, operation=Python())
