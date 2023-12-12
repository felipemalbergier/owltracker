from tkinter.tix import TList
from plyer import notification
import time

class Notification:
    APP_NAME = "Owltracker"
    ICON_PATH = "brain.ico"
    task_notification_start_time = time.time()

    LIMIT_IDLE_TIME_WITH_TASK = 15 * 60  # in seconds
    LIMIT_TIME_NO_TASK_SELECTED = 15 * 60  # in seconds
    LIMIT_TIME_WITH_TASK_SELECTED = 30 * 60 # in seconds

    def __init__(self) -> None:
        pass
    
    def _send_notification(self, title, message, timeout):
        notification.notify(
            title=title,
            message=message,
            app_name=self.APP_NAME,
            app_icon=self.ICON_PATH,
            timeout=timeout,
        )
    
    def notify_working_same_task(self, task_name):
        title=f'Still working on {task_name}'
        message="Don't forget to update on Owlltracker"
        timeout=5,
        self._send_notification(title, message, timeout)
        
        self.task_notification_start_time = time.time()

    def notify_not_working_task(self):
        title='Are you working on a task?'
        message="Don't forget to add to Owlltracker"
        timeout=5
        self._send_notification(title,message, timeout)
        
        self.task_notification_start_time = time.time()
    
    def notify_updated_time_integration(self, integration, task_name):
        title=f"{integration.title()} task time updated"
        message=f"Task name: {task_name}"
        timeout=5
        self._send_notification(title, message, timeout)

    def notify_error_updated_time_integration(self, integration, task_name, response_text):
        title=f"Could not update {integration} task time"
        message=f"Task name: {task_name}. Response: {response_text}"
        timeout=5
        self._send_notification(title, message, timeout)

if __name__ == "__main__":
    n = Notification()
    n.notify_working_same_task("sd")