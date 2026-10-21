from typing import Final
from verdog_runtime.declarations import EdgeDefinition, NumericalEffectObservation, NumericalFeatureEffect
from verdog_ai.cxxcompilediet.subroutines.propose import EDGE_IDS, NODE_IDS, FEATURE_IDS
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.change.visit.begin__change import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.begin__change, source=NODE_IDS.begin, target=NODE_IDS.change, name='begin to change', conditions=(), effects=(NumericalFeatureEffect(feature_id=FEATURE_IDS.repairs_left, observation=NumericalEffectObservation.UNCONSTRAINED),), visit=VISIT)
