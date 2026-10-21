from typing import Final
from verdog_runtime.declarations import FeatureDefinition, FeatureKind
from verdog_ai.cxxcompilediet.subroutines.main import FEATURE_IDS, StateScope

FEATURE: Final[FeatureDefinition[int, StateScope]] = FeatureDefinition(id=FEATURE_IDS.ideas_left, label='ideas_left', description='New ideas that may still fail in a row (explore_failures); refilled by a kept change.', kind=FeatureKind.INTEGER)
