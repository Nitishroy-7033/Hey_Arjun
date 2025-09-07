import json
import logging

logger = logging.getLogger(__name__)

ROUTER_PROMPT ="""
You are an intent router for a personal assistant.
Available actions:
- chat: for general conversation
- tool: when user wants a system action

Tools:
1. open_app(app_name): Opens applications. Available apps: chrome, firefox, edge, vscode, visual studio, 
   word, excel, powerpoint, notepad, calculator, file explorer, command prompt, powershell, task manager, 
   control panel, settings
   
2. set_volume(level): Sets system volume (0-100 percent)

3. shutdown_computer(delay_seconds=60): Schedules system shutdown with delay

4. cancel_shutdown(): Cancels a scheduled shutdown

5. sleep_computer(): Puts computer to sleep mode

6. create_folder(folder_name, path=None): Creates a new folder at specified path or desktop

7. lock_computer(): Locks the computer

8. unlock_computer(password): Attempts to unlock with password (for demo only)

9. restart_computer(delay_seconds=60): Schedules system restart with delay

Rules:
- Always respond in JSON only.
- If tool needed: {"action": "tool", "tool": "tool_name", "arguments": {"arg1": "value1"}}
- If just chat: {"action": "chat", "response": "your response"}
- Never include extra text outside the JSON.
- Parse user intent carefully to select the right tool and arguments.
"""

def decide_action(chat, user_input: str):
    """ Ask LLM to decide whether to chat or call a tool """
    try:
        # For API key related errors, we need to handle them directly
        if "I can't access my secret powers" in chat.conversation_history[-1].get("content", ""):
            logger.warning("API key issue detected, informing user")
            return {
                "action": "chat",
                "response": "There seems to be an issue with my API key. Please check the OPENROUTER_API_KEY in your .env file and make sure it's valid."
            }
        
        response = chat.chat(f"{ROUTER_PROMPT}\nUser Input: {user_input}", stream=False)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON response: {response}")
            return {"action": "chat", "response": "I'm processing your request as a normal conversation since I couldn't parse my own thinking."}
            
    except Exception as e:
        logger.error(f"Error in router: {str(e)}")
        return {"action": "chat", "response": "I'm having trouble connecting to my brain right now. There might be an issue with my API key or connection."}