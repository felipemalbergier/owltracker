from abc import ABC, abstractmethod
import requests


class Integration(ABC):
    def __init__(self) -> None:
        pass

    @staticmethod
    def request_api(method, url, headers, params=None, payload=None):
        response = requests.request(method, url, headers=headers, params=params, json=payload)
        return response

    @abstractmethod
    def get_list_tasks(self): pass

    @abstractmethod
    def update_time_task(self): pass

    def get_user_settings_name(self):
        return f"-{self.get_class_name().upper()}_TASKS-"

    def get_class_name(self):
        return self.__class__.__name__
