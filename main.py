#!/usr/bin/env python3
"""
Eva Voice Assistant - Main Application
A voice-controlled AI assistant with system integration capabilities.
"""

import time
import logging
import os
from typing import Optional, Dict, Any

# Core imports
from core.listener import listen_voice, check_internet_connection, listen_for_wake_word
from core.text_to_speech import text_to_speech
from core.chat_openrouter import OpenRouterChat

# Configuration imports
from configs.config import Configs
from configs.constant import Constants
from configs.messages import ErrorMessages, InfoMessages, DefaultResponses

# Router and tools
from router import decide_action
from tools.system_tools import SystemToolManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceAssistant:
    """Main Voice Assistant Class"""
    
    def __init__(self):
        self.configs = Configs()
        self.chat: Optional[OpenRouterChat] = None
        self.tool_manager = SystemToolManager()
        
    def check_api_key(self) -> bool:
        """Check if OpenRouter API key is valid"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv("OPENROUTER_API_KEY")
            return bool(api_key)
        except Exception as e:
            logger.error(f"Error checking API key: {e}")
            return False
    
    def initialize_chat(self) -> bool:
        """Initialize the chat system"""
        try:
            self.chat = OpenRouterChat()
            return True
        except ValueError:
            text_to_speech(ErrorMessages.API_KEY_ISSUE)
            return False
        except Exception as e:
            logger.error(f"Chat initialization error: {e}")
            text_to_speech(ErrorMessages.STARTUP_ERROR)
            return False
    
    def announce_startup(self):
        """Announce that the assistant is ready"""
        text_to_speech(
            InfoMessages.ASSISTANT_STARTING.format(
                assistant_name=self.configs.ASSISTANT_NAME
            )
        )
        text_to_speech(
            InfoMessages.ASSISTANT_READY.format(
                assistant_name=self.configs.ASSISTANT_NAME
            )
        )
    
    def handle_network_error(self):
        """Handle network connectivity issues"""
        text_to_speech(InfoMessages.WAITING_FOR_NETWORK)
        time.sleep(Constants.NETWORK_ERROR_DELAY)
    
    def handle_voice_input(self) -> Optional[str]:
        """Get and validate voice input"""
        text = listen_voice()
        
        if text == Constants.NETWORK_ERROR:
            text_to_speech(ErrorMessages.NETWORK_CONNECTION_ERROR)
            time.sleep(Constants.NETWORK_ERROR_DELAY)
            return None
            
        if not text:
            text_to_speech(ErrorMessages.AUDIO_NOT_UNDERSTOOD)
            return None
            
        return text
    
    def process_user_input(self, user_input: str):
        """Process user input and decide on action"""
        if not self.chat:
            text_to_speech(ErrorMessages.STARTUP_ERROR)
            return
            
        decision = decide_action(self.chat, user_input)
        
        if decision["action"] == Constants.ACTION_TOOL:
            self.handle_tool_action(decision)
        elif decision["action"] == Constants.ACTION_CHAT:
            self.handle_chat_response(decision)
    
    def handle_tool_action(self, decision: Dict[str, Any]):
        """Handle tool-based actions"""
        tool_name = decision.get("tool")
        arguments = decision.get("arguments", {})
        
        try:
            result = self.tool_manager.execute_tool(tool_name, arguments)
            if result:
                text_to_speech(result)
        except Exception as e:
            logger.error(f"Tool execution error: {e}")
            text_to_speech(
                ErrorMessages.TOOL_EXECUTION_ERROR.format(
                    tool_name=tool_name, 
                    error=str(e)
                )
            )
    
    def handle_chat_response(self, decision: Dict[str, Any]):
        """Handle chat-based responses"""
        response = decision.get("response", DefaultResponses.FALLBACK_RESPONSE)
        text_to_speech(response)
    
    def run_main_loop(self):
        """Main application loop"""
        try:
            while True:
                # Listen for wake word
                if listen_for_wake_word(wake_word=self.configs.ASSISTANT_NAME.lower()):
                    text_to_speech(InfoMessages.LISTENING)
                    
                    # Check internet connection
                    if not check_internet_connection():
                        self.handle_network_error()
                        continue
                    
                    # Get and process voice input
                    user_input = self.handle_voice_input()
                    if user_input:
                        self.process_user_input(user_input)
                    
                    time.sleep(Constants.POST_ACTION_DELAY)
                
                time.sleep(Constants.DEFAULT_SLEEP_DELAY)
                
        except KeyboardInterrupt:
            text_to_speech(InfoMessages.GOODBYE_MESSAGE)
            logger.info("Application terminated by user")
    
    def start(self):
        """Start the voice assistant"""
        logger.info("Starting Eva Voice Assistant...")
        
        # Check API key
        if not self.check_api_key():
            text_to_speech(ErrorMessages.API_KEY_MISSING)
            return
        
        # Initialize chat system
        if not self.initialize_chat():
            return
        
        # Announce startup
        self.announce_startup()
        
        # Start main loop
        self.run_main_loop()


def main():
    """Main entry point"""
    assistant = VoiceAssistant()
    assistant.start()


if __name__ == "__main__":
    main()