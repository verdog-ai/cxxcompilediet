from typing import Final
from verdog_runtime.declarations import EdgeDefinition, NumericalEffectObservation, NumericalFeatureEffect
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS, FEATURE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.route.visit.budget__route import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.budget__route, source=NODE_IDS.budget, target=NODE_IDS.route, name='budget to route', conditions=(), effects=(NumericalFeatureEffect(feature_id=FEATURE_IDS.changes_left, observation=NumericalEffectObservation.UNCONSTRAINED), NumericalFeatureEffect(feature_id=FEATURE_IDS.rules_left, observation=NumericalEffectObservation.UNCONSTRAINED), NumericalFeatureEffect(feature_id=FEATURE_IDS.ideas_left, observation=NumericalEffectObservation.UNCONSTRAINED)), visit=VISIT)
