## install these package 
`pip install SpeechRecognition pyttsx3 pyaudio`


# Hey Eva - Voice Assistant

A conversational AI assistant that uses speech recognition and modern language models to provide a natural, voice-controlled computing experience.

## 🌟 Features

- **
*: Talk naturally with Eva using speech recognition
- **Natural Conversation**: Powered by large language models through OpenRouter API
- **System Control**: Control your computer with voice commands
- **Multilingual Support**: Includes support for English and Hindi responses
- **Smart Context**: Maintains conversation history for contextual responses

## 🛠️ System Tools

Eva can perform various system operations:

- **Open Applications**: Launch browsers, productivity tools, and system utilities
- **Volume Control**: Adjust system volume with voice commands
- **Power Management**: Shutdown, restart, or sleep your computer
- **File Operations**: Create folders and manage files
- **Security**: Lock your computer with voice commands

## 🔧 Technical Architecture

- **Core Components**:
  - Speech recognition using Google's speech recognition API
  - LLM-based reasoning via OpenRouter API
  - Text-to-speech using pyttsx3 and Google TTS
  - Intent routing for action selection

- **Decision Making**:
  - Smart intent detection to differentiate between conversation and tool requests
  - Structured JSON responses for tool execution
  - Error handling and graceful fallbacks

## 📋 Requirements

- Python 3.8+
- OpenRouter API key
- Internet connection for speech recognition and LLM services
- Windows OS (for system tools)

## 🚀 Setup and Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/hey-Eva.git
   cd hey-Eva
   ```

2. Install requirements
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key
   ```

4. Run the assistant
   ```bash
   python main.py
   ```

## 📢 Usage

1. Start the assistant with `python main.py`
2. Wait for the "Eva is now online and ready to assist you" message
3. Speak your commands or questions
4. Eva will respond with speech and text

### Example Commands

- "Open Chrome"
- "Set volume to 50 percent"
- "Create a new folder called Projects"
- "What's the weather like today?"
- "Tell me a joke"
- "Shutdown my computer in 5 minutes"

## 🔄 Customization

You can customize Eva by editing:

- `core/chat_openrouter.py` - Change the personality and system prompt
- `tools/system_tools.py` - Add more system tools and capabilities
- `router.py` - Adjust decision-making logic

## ⚠️ Limitations

- Some system functions are Windows-specific
- Speech recognition requires internet connectivity
- API key must be valid and have sufficient credits

## 📜 License

[MIT License](LICENSE)



# Demo

# Eva AI Assistant - Demo

![Eva Demo](https://your-image-url-here.com/Eva-demo.png)

Hey everyone! Today I'm super excited to introduce you to my own AI assistant — Eva. It's still in the very early stage, but guess what? Eva can already chat with me and even control my laptop. Let me give you a quick demo 🚀.

## 🎬 Demo Conversation

👨‍💻: "Hello Eva, how are you today?"

👨‍💻: "I'm not feeling well… can you suggest what I should do?"

👨‍💻: "The sound is too low, can you increase my volume to 100%?"

👨‍💻: "I need to jot something down quickly, can you open Notepad?"


👨‍💻: "So Eva, what else can you do?"

## ✨ Features available in Version 1:

- **Natural Conversation**: Talk naturally in English + Hindi
- **Application Control**: Open system applications (Chrome, Notepad, VS Code, etc.)
- **System Management**: Control system volume, shutdown, restart, sleep
- **Basic Conversations**: General knowledge and casual chatting
- **Smart Decision Making**: Uses decision logic to determine when to call a tool or just chat (MCP)

## 🚀 Coming in Next Updates:

- **Interruption Handling**: We can interrupt in between conversation
- **Note Taking**: Create note way saying all details
- **RAG System**: Read your files and code, and suggest improvements

## 🔧 Technical Stack

- **Voice Recognition**: Google Speech Recognition
- **Language Model**: DeepSeek Chat via OpenRouter API
- **Text-to-Speech**: pyttsx3 and Google TTS
- **Decision Framework**: Custom routing logic with MCP principles

## 🛠️ Setup & Installation

1. Clone the repository
2. Install requirements:
   ```
   pip install SpeechRecognition pyttsx3 pyaudio
   pip install -r requirements.txt
   ```
3. Add your OpenRouter API key to `.env` file
4. Run with:
   ```
   python main.py
   ```

## 📝 Feedback

This is an early version and I'm actively developing more features. If you try it out, I'd love to hear your thoughts and suggestions!

## 🔗 Links

- [GitHub Repository](https://github.com/yourusername/Eva)
- [Development Log](https://your-blog-or-site.com)
- [Contact Me](mailto:your-email@example.com)

