from typing import Final
from verdog_runtime.declarations import EdgeDefinition, NumericalEffectObservation, NumericalFeatureEffect
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS, FEATURE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.route.visit.idea_failed import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.idea_failed, source=NODE_IDS.tally, target=NODE_IDS.route, name='idea failed', conditions=(), effects=(NumericalFeatureEffect(feature_id=FEATURE_IDS.ideas_left, observation=NumericalEffectObservation.DECREASES),), visit=VISIT)
