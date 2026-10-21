from typing import Final
from verdog_runtime.declarations import FeatureDefinition, FeatureKind
from verdog_ai.cxxcompilediet.subroutines.main import FEATURE_IDS, StateScope

FEATURE: Final[FeatureDefinition[int, StateScope]] = FeatureDefinition(id=FEATURE_IDS.rules_left, label='rules_left', description='Rounds without a kept change before new ideas (stagnation); refilled by a kept change.', kind=FeatureKind.INTEGER)
