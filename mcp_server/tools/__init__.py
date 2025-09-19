"""
MCP Tools Package

Contains MCP-compatible tool implementations for Eva voice assistant
using FastMCP with clean function-based tools and decorators.
"""

from .system_tools import (
    MCPSystemTools,
    get_tool_manager,
    open_application_tool,
    set_volume_tool,
    power_control_tool,
    file_operations_tool,
    cancel_shutdown_tool,
    get_available_applications,
    get_tool_descriptions
)

__all__ = [
    "MCPSystemTools",
    "get_tool_manager",
    "open_application_tool",
    "set_volume_tool",
    "power_control_tool", 
    "file_operations_tool",
    "cancel_shutdown_tool",
    "get_available_applications",
    "get_tool_descriptions"
]