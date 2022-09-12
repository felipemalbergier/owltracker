import requests
import yaml
import time

from owltracker.data.integrations.clickup.task_clickup import ClickupTask
from owltracker.data.integrations.integration import Integration

with open("config.json") as f:
    config = yaml.safe_load(f)

class Clickup(Integration):
    BASE_URL = "https://api.clickup.com/api/v2/"
    WORKSPACE_ID = config['workspace_id']

    def __init__(self) -> None:
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': config['api_token']
        }

    def get_list_tasks(self) -> list[dict]:
        # TODO Implement grequests
        params = {"statuses[0]": 'doing'}
        url = self.BASE_URL + f"/team/{self.WORKSPACE_ID}/task?"
        response = self.request_api("GET", url, self.headers, params=params)
        
        tasks = list()
        for task in response.json().get('tasks', {}):
            processed_task = ClickupTask(original_data=task)
            tasks.append(processed_task)
        return tasks
        

    def update_time_task(self, task_id: str, task_time: float) -> requests.models.Response:
        url = f"https://api.clickup.com/api/v2/team/{self.WORKSPACE_ID}/time_entries/"
        payload={
        "description": "from owltracker",
        "tags": [
            {
            "name": "owltracker",
            "tag_bg": "#BF55EC",
            "tag_fg": "#FFFFFF"
            }
        ],
        "start": int(time.time() - task_time) * 1000,
        "duration": int(task_time * 1000),
        "tid": f"{task_id}"
        }
        response = self.request_api("POST", url, headers=self.headers, payload=payload)
        return response

if __name__ == "__main__":
    clickup = Clickup()
    tasks = clickup.get_list_tasks()