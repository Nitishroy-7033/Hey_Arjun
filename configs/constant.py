class Constants:
    # HTTP Status Codes
    SUCCESS_STATUS_CODE = 200
    ERROR_STATUS_CODE = 500
    
    # Timing Constants
    DEFAULT_SLEEP_DELAY = 0.1
    NETWORK_ERROR_DELAY = 5
    POST_ACTION_DELAY = 0.5
    
    # Volume Settings
    DEFAULT_VOLUME_STEP = 10
    
    # Network Settings
    GOOGLE_DNS_SERVER = "8.8.8.8"
    DNS_PORT = 53
    NETWORK_TIMEOUT = 3
    
    # Audio Settings
    DEFAULT_TTS_RATE = 150
    DEFAULT_TTS_VOLUME = 2.0
    TEMP_AUDIO_FILENAME = "temp_voice.mp3"
    
    # File Extensions
    AUDIO_FILE_EXTENSION = ".mp3"
    
    # Default Delays
    DEFAULT_SHUTDOWN_DELAY = 60
    DEFAULT_RESTART_DELAY = 60
    
    # Application Paths
    APP_PATHS = {
        # Browsers
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        
        # Development tools
        "vscode": r"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        "visual studio": r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe",
        
        # Office apps
        "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        "excel": r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
        "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
        
        # System tools
        "notepad": r"C:\Windows\System32\notepad.exe",
        "calculator": r"C:\Windows\System32\calc.exe",
        "file explorer": r"C:\Windows\explorer.exe",
        "command prompt": r"C:\Windows\System32\cmd.exe",
        "powershell": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
        "task manager": r"C:\Windows\System32\Taskmgr.exe",
        "control panel": r"C:\Windows\System32\control.exe",
        "settings": r"ms-settings:",
    }
    
    # Tool Names
    TOOL_OPEN_APP = "open_app"
    TOOL_SET_VOLUME = "set_volume"
    TOOL_SHUTDOWN_COMPUTER = "shutdown_computer"
    TOOL_CANCEL_SHUTDOWN = "cancel_shutdown"
    TOOL_SLEEP_COMPUTER = "sleep_computer"
    TOOL_CREATE_FOLDER = "create_folder"
    TOOL_LOCK_COMPUTER = "lock_computer"
    TOOL_UNLOCK_COMPUTER = "unlock_computer"
    TOOL_RESTART_COMPUTER = "restart_computer"
    
    # Action Types
    ACTION_TOOL = "tool"
    ACTION_CHAT = "chat"
    
    # Network Error Indicators
    NETWORK_ERROR = "NETWORK_ERROR"


    