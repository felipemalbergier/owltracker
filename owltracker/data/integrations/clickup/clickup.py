import requests
import time
import os

from owltracker.data.integrations.clickup.task_clickup import ClickupTask
from owltracker.data.integrations.integration import Integration

from dotenv import load_dotenv
from retry import retry

load_dotenv()


class Clickup(Integration):
    BASE_URL = "https://api.clickup.com/api/v2/"
    WORKSPACE_ID = os.getenv('workspace_id')

    def __init__(self) -> None:
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': os.getenv('api_token')
        }

    @retry(exceptions=requests.exceptions.ConnectionError, tries=2, delay=1, backoff=2)
    def get_list_tasks(self) -> list[dict]:
        params = {"statuses[0]": 'this week', 'subtasks': True}
        url = self.BASE_URL + f"/team/{self.WORKSPACE_ID}/task?"
        try: 
            response = self.request_api("GET", url, self.headers, params=params)
            response_data = response.json()
        except requests.exceptions.ConnectionError:
            response_data = {'tasks': list()}            

        tasks = list()
        for task in response_data.get('tasks', {}):
            processed_task = ClickupTask(original_data=task)
            tasks.append(processed_task)
        return tasks

    def update_time_task(self, task_id: str, task_time: float) -> requests.models.Response:
        url = f"https://api.clickup.com/api/v2/team/{self.WORKSPACE_ID}/time_entries/"
        payload = {
            "start": int(time.time() - task_time) * 1000,
            "duration": int(task_time * 1000),
            "tid": f"{task_id}"
        }
        response = self.request_api("POST", url, headers=self.headers, payload=payload)

        comment_response = self.comment_task(task_id, f"Updated time via Owltracker")
        # self.request_api("GET", url, headers=self.headers)
        return response

    def comment_task(self, task_id: str, comment: str) -> requests.models.Response:
        url = f"https://api.clickup.com/api/v2/task/{task_id}/comment"
        payload = {
            "comment_text": comment
        }
        response = self.request_api("POST", url, headers=self.headers, payload=payload)
        return response


if __name__ == "__main__":
    clickup = Clickup()
    # clickup.update_time_task("86939z5z1", 60)
    tasks = clickup.get_list_tasks()
