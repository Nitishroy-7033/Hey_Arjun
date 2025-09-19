#!/usr/bin/env python3
"""
Simple MCP Client for testing Eva Voice Assistant MCP Server
"""

import asyncio
import json
import logging
import subprocess
import sys
import os

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SimpleMCPClient:
    """Simple MCP client for testing the server"""
    
    def __init__(self):
        self.server_process = None
    
    async def start_server(self):
        """Start the MCP server as a subprocess"""
        try:
            server_path = os.path.join(os.path.dirname(__file__), "server_standalone.py")
            python_path = os.path.join(parent_dir, "arjun_env", "Scripts", "python.exe")
            
            self.server_process = subprocess.Popen(
                [python_path, server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            logger.info("MCP Server started")
            return True
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return False
    
    async def send_request(self, method: str, params: dict = None) -> dict:
        """Send a JSON-RPC request to the server"""
        if not self.server_process:
            raise RuntimeError("Server not started")
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        try:
            # Send request
            request_json = json.dumps(request) + "\n"
            self.server_process.stdin.write(request_json)
            self.server_process.stdin.flush()
            
            # Read response
            response_line = self.server_process.stdout.readline()
            if response_line:
                return json.loads(response_line.strip())
            else:
                return {"error": "No response from server"}
                
        except Exception as e:
            logger.error(f"Error sending request: {e}")
            return {"error": str(e)}
    
    async def test_list_tools(self):
        """Test listing available tools"""
        logger.info("Testing tool listing...")
        response = await self.send_request("tools/list")
        if "result" in response:
            tools = response["result"].get("tools", [])
            logger.info(f"Found {len(tools)} tools:")
            for tool in tools:
                logger.info(f"  - {tool['name']}: {tool['description']}")
        else:
            logger.error(f"Error listing tools: {response}")
    
    async def test_tool_call(self, tool_name: str, arguments: dict):
        """Test calling a specific tool"""
        logger.info(f"Testing tool call: {tool_name}")
        response = await self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        if "result" in response:
            content = response["result"].get("content", [])
            for item in content:
                if item.get("type") == "text":
                    logger.info(f"Tool result: {item['text']}")
        else:
            logger.error(f"Error calling tool: {response}")
    
    async def run_tests(self):
        """Run a series of tests"""
        if not await self.start_server():
            return
        
        # Wait a moment for server to initialize
        await asyncio.sleep(2)
        
        try:
            # Test 1: List tools
            await self.test_list_tools()
            
            # Test 2: Get available applications
            await self.test_tool_call("get_available_applications", {})
            
            # Test 3: Get system info
            await self.test_tool_call("get_system_info", {})
            
            # Test 4: Create a folder (safe test)
            await self.test_tool_call("create_folder", {
                "folder_name": "MCPTestFolder",
                "path": "desktop"
            })
            
            logger.info("All tests completed!")
            
        except Exception as e:
            logger.error(f"Test error: {e}")
        finally:
            if self.server_process:
                self.server_process.terminate()
                self.server_process.wait()
                logger.info("Server terminated")


async def main():
    """Main entry point for the test client"""
    logger.info("Starting MCP Client Tests...")
    client = SimpleMCPClient()
    await client.run_tests()


if __name__ == "__main__":
    asyncio.run(main())