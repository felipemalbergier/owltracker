from asyncio import Task
from datetime import datetime
import os
from owltracker.data.integrations.clickup.clickup import Clickup
from owltracker.data.user_settings import get_entry_user_settings, set_entry_user_settings, verify_in_user_settings
from owltracker.ui.notification import Notification

last_location_settings_format = '-LAST_LOCATION_{}-'
tasks_list_settings = 'tasks_list'


class Model:
    TIMES_FILES = os.path.join(os.path.dirname(__file__), "time_database.csv") 
    COLUMNS_TIME_FILES = ['Time Input', 'Task Name', 'Time Spent', "Integration", "Integration ID"]
    def __init__(self) -> None:
        self.integrations = {"clickup": Clickup()}
        self.notification = Notification()

    def get_tasks_list_selector(self) -> list:        
        integrations_tasks = list()
        for integration in self.integrations.values():
            integration_tasks = integration.get_list_tasks()
            integrations_tasks += integration_tasks
                    
        manually_added_tasks = get_entry_user_settings(tasks_list_settings, list())
        return manually_added_tasks + integrations_tasks

    def update_time_integration(self, task: Task, task_time: str):
        if task.integration:
            r = self.integrations[task.integration].update_time_task(task.id, task_time)
            if r.ok:
                self.notification.notify_updated_time_integration(task.integration, task)
            else:
                self.notification.notify_error_updated_time_integration(task.integration, task, r.text)
    
    def save_time(self, task: Task, time: int):
        # Add columns headers
        if not os.path.exists(self.TIMES_FILES):
            with open(self.TIMES_FILES, 'w') as f:
                f.write(";".join(self.COLUMNS_TIME_FILES))
                f.write("\n")

        # Add content
        now = datetime.now().isoformat()
        with open(self.TIMES_FILES, 'a') as f:
            f.write(";".join([now, task.title, f"{time:.0f}", task.integration, task.id]))
            f.write("\n")
        
        self.update_time_integration(task, time)
