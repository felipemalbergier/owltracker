import PySimpleGUI as sg
from owltracker.data.integrations.clickup.clickup import get_list_tasks
from owltracker.data.integrations.clickup.clickup import update_time_task

last_location_settings_format = '-LAST_LOCATION_{}-'
tasks_list_settings = 'tasks_list'
clickup_tasks_settings = '-CLICKUP_TASKS-'
integrations_settings = [clickup_tasks_settings]


def get_tasks_list_selector() -> list:
    if tasks_list_settings not in sg.user_settings():
        sg.user_settings_set_entry(tasks_list_settings, list())
    clickup_tasks = get_list_tasks()
    sg.user_settings_set_entry(clickup_tasks_settings, clickup_tasks)
    clickup_tasks = [task['name'] for task in clickup_tasks]
    return sg.user_settings_get_entry(tasks_list_settings) + clickup_tasks

def update_time_integration(task_name: str, task_time: str):
    used_task = None
    for integration_setting in integrations_settings:
        for task in sg.user_settings_get_entry(integration_setting):
            if task['name'] == task_name:
                used_task = task
                break
    
    if used_task:
        r = update_time_task(used_task['id'], task_time)
        if r.ok:
            sg.SystemTray.notify(f'{used_task["integration"]} task updated', f'{used_task["name"]}')    
        
        
def add_used_task(task_name: str) -> None:
    if task_name not in sg.user_settings_get_entry(tasks_list_settings, list()):
        updated_used_tasks_list = sg.user_settings_get_entry(tasks_list_settings, list())
        updated_used_tasks_list.append(task_name)
        sg.user_settings_set_entry(tasks_list_settings, updated_used_tasks_list)
        
def get_last_window_location(window_title):
    return sg.user_settings_get_entry(last_location_settings_format.format(window_title), (None, None))

def set_last_window_location(window_title, location):
    sg.user_settings_set_entry(last_location_settings_format.format(window_title), location)
