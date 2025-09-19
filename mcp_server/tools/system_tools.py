#!/usr/bin/env python3
"""
MCP System Tools for Eva Voice Assistant

This module provides system tools adapted for the Model Context Protocol,
using FastMCP with clean function-based tools.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.system_tools import SystemToolManager
from configs.constant import Constants
from configs.messages import SuccessMessages, ErrorMessages

logger = logging.getLogger(__name__)

# Initialize the system tool manager
_tool_manager = SystemToolManager()


def get_tool_manager() -> SystemToolManager:
    """Get the shared system tool manager instance"""
    return _tool_manager


# Direct tool functions for FastMCP compatibility
async def open_application_tool(app_name: str) -> str:
    """
    Open an application via MCP tool
    
    Args:
        app_name: Name of the application to open
        
    Returns:
        String result of the operation
    """
    try:
        if not app_name:
            return ErrorMessages.INVALID_INPUT
        
        result = _tool_manager.open_app(app_name)
        logger.info(f"MCP Tool: Opened application {app_name}")
        return result
    except Exception as e:
        error_msg = f"Failed to open application {app_name}: {str(e)}"
        logger.error(error_msg)
        return error_msg


async def set_volume_tool(level: int) -> str:
    """
    Set system volume via MCP tool
    
    Args:
        level: Volume level (0-100)
        
    Returns:
        String result of the operation
    """
    try:
        if not isinstance(level, int) or not 0 <= level <= 100:
            return "Error: Volume level must be an integer between 0 and 100"
        
        result = _tool_manager.set_volume(level)
        logger.info(f"MCP Tool: Set volume to {level}%")
        return result
    except Exception as e:
        error_msg = f"Failed to set volume: {str(e)}"
        logger.error(error_msg)
        return error_msg


async def power_control_tool(action: str, delay: int = Constants.DEFAULT_SHUTDOWN_DELAY) -> str:
    """
    Control system power operations via MCP tool
    
    Args:
        action: Power action (shutdown, restart, sleep, lock)
        delay: Delay in seconds for shutdown/restart
        
    Returns:
        String result of the operation
    """
    try:
        if not action:
            return "Error: action parameter is required"
        
        delay = int(delay) if delay is not None else Constants.DEFAULT_SHUTDOWN_DELAY
        
        if action == "shutdown":
            result = _tool_manager.shutdown_computer(delay)
            logger.info(f"MCP Tool: Initiated shutdown with {delay}s delay")
            return result
        elif action == "restart":
            result = _tool_manager.restart_computer(delay)
            logger.info(f"MCP Tool: Initiated restart with {delay}s delay")
            return result
        elif action == "sleep":
            result = _tool_manager.sleep_computer()
            logger.info("MCP Tool: Put computer to sleep")
            return result
        elif action == "lock":
            result = _tool_manager.lock_computer()
            logger.info("MCP Tool: Locked computer")
            return result
        else:
            return f"Error: Unknown power action '{action}'. Valid actions: shutdown, restart, sleep, lock"
            
    except Exception as e:
        error_msg = f"Failed to execute power action {action}: {str(e)}"
        logger.error(error_msg)
        return error_msg


async def file_operations_tool(operation: str, name: str, path: Optional[str] = None) -> str:
    """
    Perform file system operations via MCP tool
    
    Args:
        operation: File operation to perform
        name: Name of the file/folder
        path: Path where to perform the operation
        
    Returns:
        String result of the operation
    """
    try:
        if not operation:
            return "Error: operation parameter is required"
        if not name:
            return "Error: name parameter is required"
        
        if operation == "create_folder":
            # Convert 'desktop' to actual desktop path
            if path == "desktop" or path is None:
                path = os.path.join(os.path.expanduser("~"), "Desktop")
            
            result = _tool_manager.create_folder(name, path)
            logger.info(f"MCP Tool: Created folder {name} at {path}")
            return result
        else:
            return f"Error: Unknown file operation '{operation}'. Valid operations: create_folder"
            
    except Exception as e:
        error_msg = f"Failed to execute file operation {operation}: {str(e)}"
        logger.error(error_msg)
        return error_msg


async def cancel_shutdown_tool() -> str:
    """
    Cancel a scheduled shutdown via MCP tool
    
    Returns:
        String result of the operation
    """
    try:
        result = _tool_manager.cancel_shutdown()
        logger.info("MCP Tool: Cancelled scheduled shutdown")
        return result
    except Exception as e:
        error_msg = f"Failed to cancel shutdown: {str(e)}"
        logger.error(error_msg)
        return error_msg


def get_available_applications() -> Dict[str, str]:
    """
    Get list of available applications that can be opened
    
    Returns:
        Dictionary mapping application names to their descriptions
    """
    return {
        app_name: f"Open {app_name.title()}"
        for app_name in Constants.APP_PATHS.keys()
    }


def get_tool_descriptions() -> Dict[str, str]:
    """
    Get descriptions of all available MCP tools
    
    Returns:
        Dictionary mapping tool names to their descriptions
    """
    return {
        "open_application": "Open applications like Chrome, VS Code, Notepad, etc.",
        "set_system_volume": "Set system volume level (0-100%)",
        "shutdown_computer": "Shutdown computer with optional delay",
        "restart_computer": "Restart computer with optional delay",
        "sleep_computer": "Put computer to sleep mode",
        "lock_computer": "Lock the computer",
        "cancel_shutdown": "Cancel a scheduled system shutdown",
        "create_folder": "Create a new folder at specified path",
        "get_available_applications": "List all available applications",
        "get_system_info": "Get basic system information"
    }


# Legacy MCPSystemTools class for backward compatibility
class MCPSystemTools:
    """MCP-compatible system tools wrapper (legacy compatibility)"""
    
    def __init__(self):
        self.tool_manager = _tool_manager
    
    async def open_application(self, params: Dict[str, Any]) -> str:
        app_name = params.get("app_name")
        return await open_application_tool(app_name)
    
    async def set_volume(self, params: Dict[str, Any]) -> str:
        level = params.get("level")
        return await set_volume_tool(level)
    
    async def power_control(self, params: Dict[str, Any]) -> str:
        action = params.get("action")
        delay = params.get("delay", Constants.DEFAULT_SHUTDOWN_DELAY)
        return await power_control_tool(action, delay)
    
    async def file_operations(self, params: Dict[str, Any]) -> str:
        operation = params.get("operation")
        name = params.get("name")
        path = params.get("path")
        return await file_operations_tool(operation, name, path)
    
    async def cancel_shutdown(self, params: Dict[str, Any]) -> str:
        return await cancel_shutdown_tool()
    
    def get_available_applications(self) -> Dict[str, str]:
        return get_available_applications()
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        return get_tool_descriptions()


# Export the main components
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
