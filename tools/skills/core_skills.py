"""
Core Framework Skills - OpenAI Agents Framework Integration
"""
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class CoreSkillConfig:
    name: str
    description: str
    instructions: str
    triggers: List[str]
    is_executable: bool
    implementation_path: str

CORE_SKILLS: Dict[str, CoreSkillConfig] = {
    "computer-control": CoreSkillConfig(
        name="computer-control",
        description="Ability to control a computer/browser through screenshots and simulated input.",
        instructions=r"""
You have the ability to control a computer or browser.
Available Actions:
- screenshot(): Captures the current screen.
- click(x, y, button): Clicks at coordinates.
- type(text): Types text.
- keypress(keys): Simulates key presses.
- scroll(x, y, dx, dy): Scrolls the view.

Rules:
1. ALWAYS take a screenshot before and after complex actions to verify state.
2. If you are stuck, describe the visual state and ask for guidance.
""",
        triggers=["browser", "website", "screenshot", "control os", "click on", "type into"],
        is_executable=True,
        implementation_path="external/providers/openai/openai-agents-python/src/agents/computer.py"
    ),
    "mcp-integration": CoreSkillConfig(
        name="mcp-integration",
        description="Model Context Protocol (MCP) server integration.",
        instructions=r"""
You can interact with MCP servers.
- Use 'list_mcp_tools' to see available tools from external servers.
- Use 'call_mcp_tool' to execute a tool.
This allows you to access specialized data and services not built into your core.
""",
        triggers=["mcp", "mcp server", "external tool", "protocol"],
        is_executable=True,
        implementation_path="external/providers/openai/openai-agents-python/src/agents/mcp"
    ),
    "editor": CoreSkillConfig(
        name="editor",
        description="Smart code editing with linting and diff support.",
        instructions=r"""
Use the 'editor' tool for precise code modifications.
- apply_diff: Apply a unified diff to a file.
- edit_file: Full file overwrite (use only if necessary).
- read_file: Read content for editing context.
Prefer 'apply_diff' for large files to be efficient.
""",
        triggers=["edit code", "refactor", "patch", "apply diff", "modify file"],
        is_executable=True,
        implementation_path="external/providers/openai/openai-agents-python/src/agents/editor.py"
    )
}
