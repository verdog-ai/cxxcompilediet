from typing import Final
from verdog_runtime.declarations import EdgeDefinition, BooleanEffectObservation, BooleanFeatureEffect
from verdog_ai.cxxcompilediet.subroutines.propose import EDGE_IDS, NODE_IDS, FEATURE_IDS
from verdog_ai.cxxcompilediet.subroutines.propose import Output as GraphOutput
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.check import Output as SourceOutput

def check_exit_output(value: SourceOutput, /) -> GraphOutput:
    return value

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.verdict__exit, source=NODE_IDS.verdict, target=NODE_IDS.exit, name='verdict to exit', conditions=(), effects=(BooleanFeatureEffect(feature_id=FEATURE_IDS.valid, observation=BooleanEffectObservation.POSITIVE),), visit=None)
