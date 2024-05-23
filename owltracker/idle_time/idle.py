import platform
from sys import platform as sys_platform

def get_idle_time():
    """Placeholder function for getting idle time"""
    raise NotImplementedError("Function not yet implemented")

def _get_idle_time_windows():
    from owltracker.idle_time.idle_windows import get_idle_windows
    return get_idle_windows()

def _get_idle_time_linux():
    from owltracker.idle_time.idle_linux import get_idle_linux
    return get_idle_linux()

if sys_platform == "win32":
    get_idle_time = _get_idle_time_windows
elif "linux" in sys_platform:
    get_idle_time = _get_idle_time_linux
else:
    raise NotImplementedError(f"Not implemented idle time for platform: {sys_platform}")
