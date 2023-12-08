from plyer import notification
import time

class Notification:
    APP_NAME = "Owltracker"
    task_notification_start_time = time.time()

    LIMIT_IDLE_TIME_WITH_TASK = 15 * 60  # in seconds
    LIMIT_TIME_NO_TASK_SELECTED = 15 * 60  # in seconds
    LIMIT_TIME_WITH_TASK_SELECTED = 30 * 60 # in seconds

    def __init__(self) -> None:
        pass
    
    def notify_working_same_task(self, task_name):
        notification.notify(
            title=f'Still working on {task_name}',
            message="Don't forget to update on Owlltracker",
            app_name=self.APP_NAME,
            timeout=5,
        )
        self.task_notification_start_time = time.time()

    def notify_not_working_task(self):
        notification.notify(
            title='Are you working on a task?',
            message="Don't forget to add to Owlltracker",
            app_name=self.APP_NAME,
            timeout=5,
                    )
        self.task_notification_start_time = time.time()
    
    def notify_updated_time_integration(self, integration, task_name):
        notification.notify(
            title=f"{integration.title()} task time updated",
            message=f"Task name: {task_name}",
            app_name=self.APP_NAME,
            timeout=5)

    def notify_error_updated_time_integration(self, integration, task_name, response_text):
            notification.notify(
                title=f"Could not update {integration} task time",
                message=f"Task name: {task_name}. Response: {response_text}",
                app_name=self.APP_NAME,
                timeout=5)
