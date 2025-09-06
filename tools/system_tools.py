import subprocess

def open_app(app_name:str)->str:
    """Open an application using the system's default method.

    Args:
        app_name (str): The name of the application to open.

    Returns:
        str: A message indicating success or failure.
    """
    apps ={
        "chrome":r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "firefox":r"C:\Program Files\Mozilla Firefox\firefox.exe",
        "notepad":r"C:\Windows\System32\notepad.exe",
        "calculator":r"C:\Windows\System32\calc.exe",
    }
    if app_name.lower() in apps:
        try:
            subprocess.Popen(apps[app_name.lower()])
            return f"{app_name} opened successfully."
        except Exception as e:
            return f"Oops, I couldn’t open {app_name}. Error: {e}"
    else:
        return f"Sorry, I don't know how to open {app_name}."