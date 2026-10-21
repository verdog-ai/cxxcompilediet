from typing import Final
from verdog_runtime.declarations import AgentProfileParameter
from verdog_ai.cxxcompilediet.subroutines.main import PROFILE_IDS
from verdog_ai.cxxcompilediet.workflows.main.profiles.agent import INVOKER as WORKFLOW_MAIN__AGENT_INVOKER

PROFILE_PARAMETER: Final[AgentProfileParameter] = AgentProfileParameter(id=PROFILE_IDS.agent, name='agent')
RESOLVED_INVOKERS: Final = (WORKFLOW_MAIN__AGENT_INVOKER,)
