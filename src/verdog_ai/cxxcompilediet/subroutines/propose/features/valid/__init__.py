from typing import Final
from verdog_runtime.declarations import FeatureDefinition, FeatureKind
from verdog_ai.cxxcompilediet.subroutines.propose import FEATURE_IDS, StateScope

FEATURE: Final[FeatureDefinition[bool, StateScope]] = FeatureDefinition(id=FEATURE_IDS.valid, label='valid', description='Whether the check found nothing in the latest reply.', kind=FeatureKind.BOOLEAN)
