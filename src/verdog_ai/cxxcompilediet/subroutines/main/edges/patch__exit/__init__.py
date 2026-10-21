from typing import Final
from verdog_runtime.declarations import EdgeDefinition
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS
from verdog_ai.cxxcompilediet.subroutines.main import Output as GraphOutput
from verdog_ai.cxxcompilediet.subroutines.main.nodes.patch import Output as SourceOutput

def check_exit_output(value: SourceOutput, /) -> GraphOutput:
    return value

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.patch__exit, source=NODE_IDS.patch, target=NODE_IDS.exit, name='patch to exit', conditions=(), effects=(), visit=None)
