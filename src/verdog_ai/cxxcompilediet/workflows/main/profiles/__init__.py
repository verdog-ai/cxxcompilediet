from typing import Final
from verdog_runtime.declarations import AgentInvoker
from verdog_runtime.declarations.ids import AgentProfileId
from verdog_ai.cxxcompilediet.workflows.main.profiles.agent import INVOKER as AGENT_INVOKER

INVOKERS: Final[dict[AgentProfileId, AgentInvoker]] = {AgentProfileId('agent'): AGENT_INVOKER}
