import subprocess
import os
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import time

def open_app(app_name: str) -> str:
    """Open an application using the system's default method.

    Args:
        app_name (str): The name of the application to open.

    Returns:
        str: A message indicating success or failure.
    """
    apps = {
        # Browsers
        "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        
        # Development tools
        "vscode": r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getenv('USERNAME')),
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
    
    if app_name.lower() in apps:
        path = apps[app_name.lower()]
        try:
            subprocess.Popen(path)
            return f"{app_name} opened successfully."
        except Exception as e:
            return f"Oops, I couldn't open {app_name}. Error: {e}"
    else:
        return f"Sorry, I don't know how to open {app_name}."

def set_volume(level: int) -> str:
    """Set system volume to a specific percentage.
    
    Args:
        level (int): Volume level as percentage (0-100)
        
    Returns:
        str: Success or failure message
    """
    try:
        if not 0 <= level <= 100:
            return f"Volume level must be between 0 and 100, got {level}"
            
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Convert percentage to logarithmic scale used by Windows
        # -65.25 to 0 is Windows volume range in dB
        if level == 0:
            # Special case for mute
            volume_scalar = -65.25
        else:
            volume_scalar = -65.25 * (1 - (level / 100)) ** 0.5
            
        volume.SetMasterVolumeLevel(volume_scalar, None)
        return f"Volume set to {level}%"
    except Exception as e:
        return f"Failed to set volume: {str(e)}"

def shutdown_computer(delay_seconds: int = 60) -> str:
    """Shutdown the computer with a delay.
    
    Args:
        delay_seconds (int): Delay before shutdown in seconds
        
    Returns:
        str: Message confirming shutdown initiated
    """
    try:
        subprocess.Popen(f"shutdown /s /t {delay_seconds}", shell=True)
        return f"Computer will shut down in {delay_seconds // 60} minutes and {delay_seconds % 60} seconds."
    except Exception as e:
        return f"Failed to initiate shutdown: {str(e)}"

def cancel_shutdown() -> str:
    """Cancel a scheduled shutdown.
    
    Returns:
        str: Message confirming shutdown cancelled
    """
    try:
        subprocess.Popen("shutdown /a", shell=True)
        return "Scheduled shutdown has been canceled."
    except Exception as e:
        return f"Failed to cancel shutdown: {str(e)}"

def sleep_computer() -> str:
    """Put the computer to sleep.
    
    Returns:
        str: Message confirming sleep mode initiated
    """
    try:
        subprocess.Popen("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
        return "Putting computer to sleep..."
    except Exception as e:
        return f"Failed to sleep computer: {str(e)}"

def create_folder(folder_name: str, path: str = None) -> str:
    """Create a new folder at the specified path or desktop.
    
    Args:
        folder_name (str): Name of the folder to create
        path (str, optional): Path where to create folder. If None, creates on desktop.
        
    Returns:
        str: Success or failure message
    """
    try:
        if not path:
            # Default to desktop if no path specified
            path = os.path.join(os.path.expanduser("~"), "Desktop")
            
        folder_path = os.path.join(path, folder_name)
        
        # Check if folder already exists
        if os.path.exists(folder_path):
            return f"Folder '{folder_name}' already exists at {path}"
            
        os.makedirs(folder_path)
        return f"Folder '{folder_name}' created successfully at {path}"
    except Exception as e:
        return f"Failed to create folder: {str(e)}"

def lock_computer() -> str:
    """Lock the computer.
    
    Returns:
        str: Message confirming computer locked
    """
    try:
        ctypes.windll.user32.LockWorkStation()
        return "Computer locked."
    except Exception as e:
        return f"Failed to lock computer: {str(e)}"

def unlock_computer(password: str) -> str:
    """Attempt to unlock the computer with password.
    
    Args:
        password (str): Password to unlock computer
        
    Returns:
        str: Message about unlock attempt
    """
    # This is a security-sensitive function, so we'll just simulate it
    # Real implementation would be dangerous as storing passwords in code is bad practice
    
    # Hardcoded password for demonstration only
    CORRECT_PASSWORD = "7033"  # NEVER do this in production!
    
    if password == CORRECT_PASSWORD:
        return "Password accepted. Note: For security reasons, actual unlocking requires system integration."
    else:
        return "Incorrect password. Access denied."

def restart_computer(delay_seconds: int = 60) -> str:
    """Restart the computer with a delay.
    
    Args:
        delay_seconds (int): Delay before restart in seconds
        
    Returns:
        str: Message confirming restart initiated
    """
    try:
        subprocess.Popen(f"shutdown /r /t {delay_seconds}", shell=True)
        return f"Computer will restart in {delay_seconds // 60} minutes and {delay_seconds % 60} seconds."
    except Exception as e:
        return f"Failed to initiate restart: {str(e)}"

if __name__ == "__main__":
    # Test some functions
    print(open_app("notepad"))
    print(set_volume(50))
    print(create_folder("evaTestfolder"))