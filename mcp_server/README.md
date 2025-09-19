# Eva Voice Assistant - MCP Server Documentation

## Overview

The Eva Voice Assistant MCP (Model Context Protocol) Server provides system control capabilities through a standardized protocol interface. This allows integration with Claude Desktop, other MCP-compatible clients, and custom applications.

## Features

The MCP server provides the following tools:

### System Control Tools
- **open_application**: Open applications like Chrome, VS Code, Notepad, etc.
- **set_system_volume**: Set system volume level (0-100%)
- **shutdown_computer**: Shutdown computer with optional delay
- **restart_computer**: Restart computer with optional delay  
- **sleep_computer**: Put computer to sleep mode
- **lock_computer**: Lock the computer
- **cancel_shutdown**: Cancel a scheduled system shutdown

### File Operations
- **create_folder**: Create a new folder at specified path

### Information Tools
- **get_available_applications**: List all available applications
- **get_system_info**: Get basic system information and server status

## Installation

1. **Install Dependencies**:
   ```bash
   pip install mcp pycaw comtypes
   ```

2. **Verify Installation**:
   ```bash
   python -c "from mcp.server import Server; print('MCP installed successfully')"
   ```

## Running the Server

### Standalone Mode
```bash
# Run the standalone MCP server
python mcp_server/server_standalone.py
```

### With Claude Desktop

1. **Add to Claude Desktop Config**:
   Create or edit `%APPDATA%\Claude\claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "eva-voice-assistant": {
         "command": "python",
         "args": ["D:/Hey_Arjun/mcp_server/server_standalone.py"],
         "env": {}
       }
     }
   }
   ```

2. **Restart Claude Desktop**: The Eva tools will be available in Claude conversations.

## Usage Examples

### Tool Schemas

Each tool has a specific input schema:

#### open_application
```json
{
  "app_name": "chrome"
}
```

#### set_system_volume
```json
{
  "level": 75
}
```

#### shutdown_computer
```json
{
  "delay_seconds": 120
}
```

#### create_folder
```json
{
  "folder_name": "MyNewFolder",
  "path": "C:/Users/Username/Desktop"
}
```

### Available Applications

The following applications can be opened:
- **Browsers**: chrome, firefox, edge
- **Development**: vscode, visual studio
- **Office**: word, excel, powerpoint
- **System**: notepad, calculator, file explorer, command prompt, powershell, task manager, control panel, settings

## Testing

Run the included test client to verify functionality:

```bash
python mcp_server/test_client.py
```

This will:
1. Start the MCP server
2. List available tools
3. Test safe operations (get info, create folder)
4. Display results

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure all dependencies are installed
   - Check Python path configuration

2. **Permission Errors**:
   - Run as administrator for system operations
   - Check file/folder permissions

3. **Application Not Found**:
   - Verify application is installed
   - Check path in Constants.APP_PATHS

### Logging

The server logs all operations to help with debugging:
- Tool calls and results
- Error messages with stack traces
- Server startup and shutdown events

## Security Considerations

⚠️ **Important Security Notes**:

- The MCP server provides direct system access
- Only run with trusted clients
- Review tool calls before execution
- Consider running in a restricted environment for testing

### Safe Testing

For safe testing, use these non-destructive tools:
- `get_available_applications`
- `get_system_info`
- `create_folder` (in safe locations)
- `set_system_volume` (with reasonable levels)

## Integration with Eva Voice Assistant

The MCP server is designed to work alongside the main Eva Voice Assistant:

1. **Shared Configuration**: Uses the same constants and messages
2. **Tool Compatibility**: Implements the same system tools
3. **Independent Operation**: Can run separately from the voice assistant

## Architecture

```
Eva Voice Assistant
├── main.py (Voice Assistant)
├── mcp_server/
│   ├── server_standalone.py (MCP Server)
│   ├── test_client.py (Test Client)
│   └── tools/ (MCP Tool Implementations)
├── configs/ (Shared Configuration)
└── tools/ (Core System Tools)
```

## API Reference

The MCP server implements the Model Context Protocol specification:

- **Initialization**: Standard MCP handshake
- **Tool Discovery**: `tools/list` method
- **Tool Execution**: `tools/call` method
- **Error Handling**: Standard JSON-RPC error responses

For detailed MCP specification, see: [Model Context Protocol](https://modelcontextprotocol.io/)

## Future Enhancements

Planned improvements:
- Additional system tools (process management, network info)
- Resource providers for file access
- Prompt templates for common operations
- Enhanced security and permission controls
- Real-time system monitoring capabilities