from typing import Final
from verdog_runtime.declarations import FeatureDefinition, FeatureKind
from verdog_ai.cxxcompilediet.subroutines.main import FEATURE_IDS, StateScope

FEATURE: Final[FeatureDefinition[int, StateScope]] = FeatureDefinition(id=FEATURE_IDS.changes_left, label='changes_left', description='Changes the run may still keep (max_changes minus the kept ones).', kind=FeatureKind.INTEGER)
