from typing import Final
from verdog_runtime.declarations import Feature, FeatureNodeDefinition
from verdog_ai.cxxcompilediet.subroutines.propose import NODE_IDS

NODE: Final[FeatureNodeDefinition] = FeatureNodeDefinition(id=NODE_IDS.begin, name='begin', operation=Feature())
