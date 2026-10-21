from typing import Final
from verdog_runtime.declarations import EdgeDefinition, NumericalConditionObservation, NumericalFeatureCondition
from verdog_ai.cxxcompilediet.subroutines.main import EDGE_IDS, NODE_IDS, FEATURE_IDS
from verdog_ai.cxxcompilediet.subroutines.main.nodes.patch.visit.ideas_done import VISIT

EDGE: Final[EdgeDefinition] = EdgeDefinition(id=EDGE_IDS.ideas_done, source=NODE_IDS.route, target=NODE_IDS.patch, name='ideas done', conditions=(NumericalFeatureCondition(feature_id=FEATURE_IDS.changes_left, observation=NumericalConditionObservation.GREATER_ZERO), NumericalFeatureCondition(feature_id=FEATURE_IDS.ideas_left, observation=NumericalConditionObservation.EQUAL_ZERO)), effects=(), visit=VISIT)
