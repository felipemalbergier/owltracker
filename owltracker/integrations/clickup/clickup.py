import requests
import json
import time


with open("config.json") as f:
    config = json.load(f)

BASE_URL = "https://api.clickup.com/api/v2/"
LIST_IDS = [180856365, # freelancing
        180856325, # projects
        180856407] # personal
WORKSPACE_ID = 31075257
TASK_INFORMATION = ['id', 'name', 'team_id', 'list']
headers = {
    'Content-Type': 'application/json',
    'Authorization': config['api_token']
}



def get_list_tasks() -> list[dict]:
    # TODO Implement grequests
    payload={}
    tasks = list()
    for list_id in LIST_IDS:
        url = BASE_URL + "list/{list_id}/task".format(list_id=list_id)
        response = requests.request("GET", url, headers=headers, data=payload)
        for task in response.json().get('tasks', {}):
            task_to_return = {info: task[info] for info in TASK_INFORMATION}
            task_to_return.update({'integration': "clickup"})
            tasks.append(task_to_return)
    return tasks
    

def update_time_task(task_id: str, task_time: float) -> None:
    url = f"https://api.clickup.com/api/v2/team/{WORKSPACE_ID}/time_entries/"
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
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.text)

if __name__ == "__main__":
    get_list_tasks()