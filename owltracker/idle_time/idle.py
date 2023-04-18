from sys import platform

def get_idle_time():
    # defined below
    pass

if platform == "win32":
    from owltracker.idle_time.idle_windows import get_idle_windows
    get_idle_time = get_idle_windows
elif "linux" in platform:
    from idle_linux import get_idle_linux
    get_idle_time = get_idle_linux
else:
    raise NotImplementedError(f"Not implemented idle time for platform: {platform}")
    