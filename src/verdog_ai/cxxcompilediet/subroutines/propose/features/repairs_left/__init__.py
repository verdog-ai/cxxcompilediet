from typing import Final
from verdog_runtime.declarations import FeatureDefinition, FeatureKind
from verdog_ai.cxxcompilediet.subroutines.propose import FEATURE_IDS, StateScope

FEATURE: Final[FeatureDefinition[int, StateScope]] = FeatureDefinition(id=FEATURE_IDS.repairs_left, label='repairs_left', description='Replies the check may still send back with its findings.', kind=FeatureKind.INTEGER)
