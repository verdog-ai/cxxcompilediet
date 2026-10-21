from typing import Final
from verdog_runtime.declarations import EdgeDefinition, NumericalConditionObservation, NumericalFeatureCondition, BooleanEffectObservation, BooleanFeatureEffect, NumericalEffectObservation, NumericalFeatureEffect
from verdog_ai.cxxcompilediet.subroutines.propose import EDGE_IDS, NODE_IDS, FEATURE_IDS
from verdog_ai.cxxcompilediet.subroutines.propose.nodes.change.visit.repair import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.repair, source=NODE_IDS.verdict, target=NODE_IDS.change, name='repair', conditions=(NumericalFeatureCondition(feature_id=FEATURE_IDS.repairs_left, observation=NumericalConditionObservation.GREATER_ZERO),), effects=(BooleanFeatureEffect(feature_id=FEATURE_IDS.valid, observation=BooleanEffectObservation.NEGATIVE), NumericalFeatureEffect(feature_id=FEATURE_IDS.repairs_left, observation=NumericalEffectObservation.DECREASES)), visit=VISIT)
