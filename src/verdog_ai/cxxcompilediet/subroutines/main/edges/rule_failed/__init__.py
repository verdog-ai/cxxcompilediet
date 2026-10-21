from typing import Final
from verdog_runtime.declarations import EdgeDefinition, NumericalEffectObservation, NumericalFeatureEffect
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS, FEATURE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.route.visit.rule_failed import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.rule_failed, source=NODE_IDS.tally, target=NODE_IDS.route, name='rule failed', conditions=(), effects=(NumericalFeatureEffect(feature_id=FEATURE_IDS.rules_left, observation=NumericalEffectObservation.DECREASES),), visit=VISIT)
