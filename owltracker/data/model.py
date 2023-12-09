from asyncio import Task
from datetime import datetime
import os
from owltracker.data.integrations.clickup.clickup import Clickup
from owltracker.data.user_settings import get_entry_user_settings, set_entry_user_settings, verify_in_user_settings
from owltracker.ui.notification import Notification

last_location_settings_format = '-LAST_LOCATION_{}-'
tasks_list_settings = 'tasks_list'


class Model:
    def __init__(self) -> None:
        self.task_sources = {"clickup": Clickup()}
        self.notification = Notification()
        self._current_tasks = list()
        self.current_task = None

    @property
    def current_tasks(self):
        self.fetch_tasks_list_selector()
        return self._current_tasks

    def fetch_tasks_list_selector(self) -> None:
        integrations_tasks = list()
        for integration in self.task_sources.values():
            integration_tasks = integration.get_list_tasks()
            integrations_tasks += integration_tasks
                    
        manually_added_tasks = get_entry_user_settings(tasks_list_settings, list())
        self._current_tasks = manually_added_tasks + integrations_tasks

    def update_time_integration(self, task_time: float):
        if self.current_task.source:
            r = self.task_sources[self.current_task.source].update_time_task(self.current_task.id, task_time)
            if r.ok:
                self.notification.notify_updated_time_integration(self.current_task.source, self.current_task)
            else:
                self.notification.notify_error_updated_time_integration(self.current_task.source, self.current_task, r.text)
