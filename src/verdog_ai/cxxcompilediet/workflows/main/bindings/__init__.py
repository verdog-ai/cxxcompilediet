from typing import Final
from verdog_ai.cxxcompilediet.workflows.main.profiles import INVOKERS
from verdog_runtime.declarations import WorkflowConfiguration

CONFIGURATION: Final[WorkflowConfiguration] = WorkflowConfiguration(profile_arguments=INVOKERS)
