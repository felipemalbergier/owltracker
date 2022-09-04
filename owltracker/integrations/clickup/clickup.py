from pickle import LIST
import requests
import json


with open("config.json") as f:
    config = json.load(f)

BASE_URL = "https://api.clickup.com/api/v2/"
LIST_IDS = [180856365, # freelancing
        180856325, # projects
        180856407] # personal
TASK_INFORMATION = ['id', 'name', 'team_id', 'list']
headers = {
    'Content-Type': 'application/json',
    'Authorization': config['api_token']
}



def get_list_tasks() -> list[dict]:
    payload={}
    tasks = list()
    for list_id in LIST_IDS:
        url = BASE_URL + "list/{list_id}/task".format(list_id=list_id)
        response = requests.request("GET", url, headers=headers, data=payload)
        for task in response.json().get('tasks', {}):
            task_to_return = {info: task[info] for info in TASK_INFORMATION}
            tasks.append(task_to_return)
    return tasks
    

def update_time_task(task_id: str, time: float) -> None:
    url = "https://api.clickup.com/api/v2/team/team_Id/time_entries/timer_id/"
    payload={}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

if __name__ == "__main__":
    get_list_tasks()