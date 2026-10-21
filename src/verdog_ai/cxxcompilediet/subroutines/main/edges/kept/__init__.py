from typing import Final
from verdog_runtime.declarations import EdgeDefinition, NumericalEffectObservation, NumericalFeatureEffect
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS, FEATURE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.route.visit.kept import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.kept, source=NODE_IDS.tally, target=NODE_IDS.route, name='change kept', conditions=(), effects=(NumericalFeatureEffect(feature_id=FEATURE_IDS.changes_left, observation=NumericalEffectObservation.DECREASES), NumericalFeatureEffect(feature_id=FEATURE_IDS.rules_left, observation=NumericalEffectObservation.UNCONSTRAINED), NumericalFeatureEffect(feature_id=FEATURE_IDS.ideas_left, observation=NumericalEffectObservation.UNCONSTRAINED)), visit=VISIT)
