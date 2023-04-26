from sys import platform

from owltracker.data.database.database import Database

class Activity:
    def __init__(self) -> None:
        if platform == "win32":
            from owltracker.data.activity_tracker.activity_tracker_windows import get_active_window_info_windows
            self.get_active_window_info = get_active_window_info_windows
        else:
            raise NotImplementedError(f"Not implemented idle time for platform: {platform}")
        
        self.db = Database()
    
    def get_active_window_info(self):
        raise NotImplementedError("Should be replaced on __init__")
    
    def log_activity(self):
        activity = self.get_active_window_info()
        self.db.add_activity(**activity)
        print(self.db.select_query("Select * from activity;"))