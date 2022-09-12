from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Task(ABC):
    id: str
    title: str
    original_data: dict
    integration: str
        
    @abstractmethod
    def __init__(self, original_data) -> None:
        pass
        
    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f"{self.integration} task | Title: {self.title}"

@dataclass
class LocalTask(Task):
    def __init__(self, task_title) -> None:
        self.title = task_title
        self.integration = ""
        self.id = ""


if __name__ == "__main__":
    t = Task()