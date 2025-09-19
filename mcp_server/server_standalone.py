#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Server for Eva Voice Assistant

This server provides system tools and capabilities through the MCP protocol,
using the official MCP library with proper tool registration.
"""

import asyncio
import logging
import os
import sys
import subprocess
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from typing import Dict, Any, Optional, Sequence

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Import only what we need to avoid circular imports
from configs.constant import Constants

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the MCP server
server = Server("eva-voice-assistant")


class SimpleMCPTools:
    """Simple MCP tools implementation without circular imports"""
    
    @staticmethod
    def open_app(app_name: str) -> str:
        """Open an application using the system's default method."""
        if app_name.lower() in Constants.APP_PATHS:
            path = Constants.APP_PATHS[app_name.lower()]
            if "{username}" in path:
                path = path.format(username=os.getenv('USERNAME', ''))
            
            try:
                subprocess.Popen(path)
                return f"{app_name} opened successfully."
            except Exception as e:
                return f"Oops, I couldn't open {app_name}. Error: {e}"
        else:
            return f"Sorry, I don't know how to open {app_name}."
    
    @staticmethod
    def set_volume(level: int) -> str:
        """Set system volume to a specific percentage."""
        try:
            if not 0 <= level <= 100:
                return f"Volume level must be between 0 and 100, got {level}"
                
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            
            # Convert percentage to logarithmic scale used by Windows
            if level == 0:
                volume_scalar = -65.25
            else:
                volume_scalar = -65.25 * (1 - (level / 100)) ** 0.5
                
            volume.SetMasterVolumeLevel(volume_scalar, None)
            return f"Volume set to {level}%"
        except Exception as e:
            return f"Failed to set volume: {str(e)}"
    
    @staticmethod
    def shutdown_computer(delay_seconds: int = 60) -> str:
        """Shutdown the computer with a delay."""
        try:
            subprocess.Popen(f"shutdown /s /t {delay_seconds}", shell=True)
            return f"Computer will shutdown in {delay_seconds} seconds."
        except Exception as e:
            return f"Failed to initiate shutdown: {str(e)}"
    
    @staticmethod
    def restart_computer(delay_seconds: int = 60) -> str:
        """Restart the computer with a delay."""
        try:
            subprocess.Popen(f"shutdown /r /t {delay_seconds}", shell=True)
            return f"Computer will restart in {delay_seconds} seconds."
        except Exception as e:
            return f"Failed to initiate restart: {str(e)}"
    
    @staticmethod
    def sleep_computer() -> str:
        """Put the computer to sleep."""
        try:
            subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
            return "Putting computer to sleep..."
        except Exception as e:
            return f"Failed to sleep computer: {str(e)}"
    
    @staticmethod
    def lock_computer() -> str:
        """Lock the computer."""
        try:
            ctypes.windll.user32.LockWorkStation()
            return "Computer locked."
        except Exception as e:
            return f"Failed to lock computer: {str(e)}"
    
    @staticmethod
    def cancel_shutdown() -> str:
        """Cancel a scheduled shutdown."""
        try:
            subprocess.Popen("shutdown /a", shell=True)
            return "Scheduled shutdown has been canceled."
        except Exception as e:
            return f"Failed to cancel shutdown: {str(e)}"
    
    @staticmethod
    def create_folder(folder_name: str, path: str = None) -> str:
        """Create a new folder at the specified path or desktop."""
        try:
            if not path:
                path = os.path.join(os.path.expanduser("~"), "Desktop")
                
            folder_path = os.path.join(path, folder_name)
            
            if os.path.exists(folder_path):
                return f"Folder '{folder_name}' already exists at {path}"
                
            os.makedirs(folder_path)
            return f"Folder '{folder_name}' created successfully at {path}"
        except Exception as e:
            return f"Failed to create folder: {str(e)}"


# Initialize tools
tools = SimpleMCPTools()


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="open_application",
            description="Open an application on the system",
            inputSchema={
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "Name of the application to open (chrome, firefox, vscode, etc.)"
                    }
                },
                "required": ["app_name"]
            }
        ),
        Tool(
            name="set_system_volume",
            description="Set the system volume level",
            inputSchema={
                "type": "object",
                "properties": {
                    "level": {
                        "type": "integer",
                        "description": "Volume level as percentage (0-100)",
                        "minimum": 0,
                        "maximum": 100
                    }
                },
                "required": ["level"]
            }
        ),
        Tool(
            name="shutdown_computer",
            description="Shutdown the computer with optional delay",
            inputSchema={
                "type": "object",
                "properties": {
                    "delay_seconds": {
                        "type": "integer",
                        "description": "Delay before shutdown in seconds",
                        "default": 60,
                        "minimum": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="restart_computer",
            description="Restart the computer with optional delay",
            inputSchema={
                "type": "object",
                "properties": {
                    "delay_seconds": {
                        "type": "integer",
                        "description": "Delay before restart in seconds",
                        "default": 60,
                        "minimum": 0
                    }
                },
                "required": []
            }
        ),
        Tool(
            name="sleep_computer",
            description="Put the computer to sleep mode",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="lock_computer",
            description="Lock the computer",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="cancel_shutdown",
            description="Cancel a scheduled system shutdown",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="create_folder",
            description="Create a new folder at the specified path",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder_name": {
                        "type": "string",
                        "description": "Name of the folder to create"
                    },
                    "path": {
                        "type": "string",
                        "description": "Path where to create the folder (default: desktop)",
                        "default": "desktop"
                    }
                },
                "required": ["folder_name"]
            }
        ),
        Tool(
            name="get_available_applications",
            description="Get a list of available applications that can be opened",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="get_system_info",
            description="Get basic system information and server status",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    """Handle tool calls"""
    try:
        if name == "open_application":
            app_name = arguments.get("app_name")
            if not app_name:
                result = "Error: app_name parameter is required"
            else:
                result = tools.open_app(app_name)
                logger.info(f"MCP Tool: Opened application {app_name}")

        elif name == "set_system_volume":
            level = arguments.get("level")
            if not isinstance(level, int) or not 0 <= level <= 100:
                result = "Error: Volume level must be an integer between 0 and 100"
            else:
                result = tools.set_volume(level)
                logger.info(f"MCP Tool: Set volume to {level}%")

        elif name == "shutdown_computer":
            delay_seconds = arguments.get("delay_seconds", 60)
            if not isinstance(delay_seconds, int) or delay_seconds < 0:
                result = "Error: delay_seconds must be a non-negative integer"
            else:
                result = tools.shutdown_computer(delay_seconds)
                logger.info(f"MCP Tool: Initiated shutdown with {delay_seconds}s delay")

        elif name == "restart_computer":
            delay_seconds = arguments.get("delay_seconds", 60)
            if not isinstance(delay_seconds, int) or delay_seconds < 0:
                result = "Error: delay_seconds must be a non-negative integer"
            else:
                result = tools.restart_computer(delay_seconds)
                logger.info(f"MCP Tool: Initiated restart with {delay_seconds}s delay")

        elif name == "sleep_computer":
            result = tools.sleep_computer()
            logger.info("MCP Tool: Put computer to sleep")

        elif name == "lock_computer":
            result = tools.lock_computer()
            logger.info("MCP Tool: Locked computer")

        elif name == "cancel_shutdown":
            result = tools.cancel_shutdown()
            logger.info("MCP Tool: Cancelled scheduled shutdown")

        elif name == "create_folder":
            folder_name = arguments.get("folder_name")
            path = arguments.get("path")
            
            if not folder_name:
                result = "Error: folder_name parameter is required"
            else:
                # Default to desktop if no path specified
                if not path or path == "desktop":
                    path = os.path.join(os.path.expanduser("~"), "Desktop")
                
                result = tools.create_folder(folder_name, path)
                logger.info(f"MCP Tool: Created folder {folder_name} at {path}")

        elif name == "get_available_applications":
            apps = Constants.APP_PATHS.keys()
            app_list = ", ".join(sorted(apps))
            result = f"Available applications: {app_list}"

        elif name == "get_system_info":
            import platform
            info = {
                "os": platform.system(),
                "os_version": platform.version(),
                "machine": platform.machine(),
                "python_version": platform.python_version(),
                "server_status": "running"
            }
            result = f"System Info: {info['os']} {info['os_version']}, Machine: {info['machine']}, Python: {info['python_version']}, Server: {info['server_status']}"

        else:
            result = f"Unknown tool: {name}"
            logger.error(f"Unknown tool called: {name}")

        return [TextContent(type="text", text=result)]

    except Exception as e:
        error_msg = f"Error executing tool {name}: {str(e)}"
        logger.error(error_msg)
        return [TextContent(type="text", text=error_msg)]


async def main():
    """Main entry point for the MCP server"""
    logger.info("Starting Eva Voice Assistant MCP Server...")
    logger.info("Available tools:")
    
    # List all available tools
    tool_names = [
        "open_application", "set_system_volume", "shutdown_computer", 
        "restart_computer", "sleep_computer", "lock_computer", 
        "cancel_shutdown", "create_folder", "get_available_applications", 
        "get_system_info"
    ]
    
    for tool_name in tool_names:
        logger.info(f"  - {tool_name}")
    
    logger.info("Server ready for connections via stdio...")
    
    # Run the server using stdio transport
    async with stdio_server() as streams:
        await server.run(
            streams[0], streams[1], 
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())