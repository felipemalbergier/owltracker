from dataclasses import dataclass
from owltracker.data.integrations.task import Task

@dataclass
class ClickupTask(Task):
    # attributes_map = { # clickup_id:
    #     "id": "id"
    # }
    
    def __init__(self, original_data) -> None:
        self.integration = 'clickup'
        self.original_data = original_data
        self.id = self.original_data['id']
        self.title = self.original_data['name']

if __name__ == "__main__":
    t = ClickupTask(original_data={"id": 1, "name": "oi"})
    