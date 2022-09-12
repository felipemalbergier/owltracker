import PySimpleGUI as sg

last_location_settings_format = '-LAST_LOCATION_{}-'
tasks_list_settings = 'tasks_list'
clickup_tasks_settings = '-CLICKUP_TASKS-'
integrations_settings = [clickup_tasks_settings]

    
def verify_in_user_settings(user_settings_name) -> bool:
    return user_settings_name in sg.user_settings()

def set_entry_user_settings(key, value) -> None:
    sg.user_settings_set_entry(key, value)
    
def get_entry_user_settings(key, default_value=None):
    return sg.user_settings_get_entry(key, default=default_value)
        
def add_used_task(task_name: str) -> None:
    used_tasks_list = get_entry_user_settings(tasks_list_settings, list())
    if task_name not in used_tasks_list:
        used_tasks_list.append(task_name)
        set_entry_user_settings(tasks_list_settings, used_tasks_list)
        
def get_last_window_location(window_title):
    return get_entry_user_settings(last_location_settings_format.format(window_title), (None, None))

def set_last_window_location(window_title, location):
    set_entry_user_settings(last_location_settings_format.format(window_title), location)
