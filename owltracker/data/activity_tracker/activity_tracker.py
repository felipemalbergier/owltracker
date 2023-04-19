from sys import platform

def log_activity():
    pass

if platform == "win32":
    from owltracker.data.activity_tracker.activity_tracker_windows import get_active_window_info_windows
    log_activity = get_active_window_info_windows
else:
    raise NotImplementedError(f"Not implemented idle time for platform: {platform}")
