from datetime import datetime
from datetime import timezone
from datetime import timedelta
from sys import platform

from owltracker.data.database.sqlite.sqlite_database import SQLiteDatabase
from owltracker.ui.view import View
from owltracker.utils import WAIT_TIME_MSECONDS


class Activity:
    def __init__(self) -> None:
        self.db = SQLiteDatabase()
        self.last_activity = dict()

        if platform == "win32":
            from owltracker.data.activity_tracker.activity_tracker_windows import get_active_window_info_windows
            self.get_active_window_info = get_active_window_info_windows
        elif platform == "linux":
            from owltracker.data.activity_tracker.activity_tracker_linux import get_active_window_info_linux
            self.get_active_window_info = get_active_window_info_linux
        else:
            raise NotImplementedError(f"Not implemented idle time for platform: {platform}")

    def get_active_window_info(self):
        raise NotImplementedError("Should be replaced on __init__")

    def log_activity(self, task=None, event=None):
        activity = self.get_active_window_info()
        if not activity:
            # log that it didn't get any activity
            print("No activity", activity)
            return
        print("Activity", activity)
        # self.db.add_activity(**activity)
        # print(self.db.select_query("Select * from activity;"))
        now = datetime.now(timezone.utc)

        # If last process name is the same - I update end datetime (verify task when implemented)
        if (self.last_activity.get('process_name') == activity.get('process_name', '') and
                self.last_activity.get('window_title') == activity.get('window_title', '')):

            end = now + timedelta(milliseconds=WAIT_TIME_MSECONDS)
            self.db.update_end_activity(end)

        else:  # (else) if last process name is null or different I add start datetime and end datetime
            if event != View.remove_idle_time:
                # this is here so we only update when not idle. This also contemplates subtracting idle time
                self.db.update_end_activity(now)
            activity['start'] = now
            activity['end'] = now + timedelta(milliseconds=WAIT_TIME_MSECONDS)
            self.db.add_new_activity(activity)

        self.last_activity = activity
