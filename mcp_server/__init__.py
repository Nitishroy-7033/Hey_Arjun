"""
Eva Voice Assistant - Model Context Protocol Server

This package provides MCP (Model Context Protocol) server functionality
for Eva voice assistant, using FastMCP with mcp.tool decorators for 
cleaner implementation and better integration.

Components:
- server.py: FastMCP server implementation with tool decorators
- tools/: MCP-compatible system tools with direct functions
"""

from .server import server, main
from .tools.system_tools import (
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

__version__ = "2.0.0"
__author__ = "Eva Assistant Team"

__all__ = [
    "server",
    "main",
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