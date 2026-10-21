from typing import Final
from verdog_runtime.agents.codex import CodexInvoker
from verdog_runtime.declarations import AgentInvoker

INVOKER: Final[AgentInvoker] = CodexInvoker(model=None, reasoning_effort='high', extra_args=('-c', 'web_search="disabled"', '-c', 'features.plugins=false'))
