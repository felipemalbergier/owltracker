import win32api

def get_idle_windows():
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0
