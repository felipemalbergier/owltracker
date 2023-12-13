from abc import ABC, abstractmethod
from dataclasses import dataclass
from dataclasses import field

@dataclass
class Task(ABC):
    id: str
    title: str
    source: str
    original_data: dict = field(repr=False, default_factory=dict)
        
    @abstractmethod
    def __init__(self, original_data) -> None:
        pass
        
    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f"{self.source} task | Title: {self.title}"

@dataclass
class LocalTask(Task):
    def __init__(self, task_title) -> None:
        self.title = task_title
        self.source = None
        self.id = None


if __name__ == "__main__":
    t = LocalTask("title")
    print(t)
    print("o")
    