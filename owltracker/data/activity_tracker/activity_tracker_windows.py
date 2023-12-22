import win32gui
import win32process
import psutil


def get_active_window_info_windows() -> dict:
    try:
        foreground_window = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(foreground_window)
        process_name = psutil.Process(pid[-1]).name()
        window_title = win32gui.GetWindowText(foreground_window)
        return {"process_name": process_name, "window_title": window_title}
    except:
        # TODO add logger
        pass
