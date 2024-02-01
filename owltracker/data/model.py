from owltracker.data.integrations.clickup.clickup import Clickup
from owltracker.data.integrations.task import LocalTask
from owltracker.data.user_settings import get_entry_user_settings
from owltracker.ui.notification import Notification
from owltracker.data.user_settings import TASKS_LIST_SETTINGS
from requests.exceptions import ConnectionError as ConnectionErrorRequests

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
            try:
                integration_tasks = integration.get_list_tasks()
                integrations_tasks += integration_tasks
            except ConnectionErrorRequests:
                if isinstance(integration, LocalTask):
                    break
                raise 

        manually_added_tasks = get_entry_user_settings(TASKS_LIST_SETTINGS, list())
        self._current_tasks = manually_added_tasks + integrations_tasks

    def update_time_integration(self, task_time: float):
        if self.current_task.source:
            r = self.task_sources[self.current_task.source].update_time_task(self.current_task.id, task_time)
            if r.ok:
                self.notification.notify_updated_time_integration(self.current_task.source, self.current_task)
            else:
                self.notification.notify_error_updated_time_integration(self.current_task.source, self.current_task,
                                                                        r.text)
