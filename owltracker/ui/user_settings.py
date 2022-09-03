import PySimpleGUI as sg

last_location_settings_format = '-LAST_LOCATION_{}-'
tasks_list_settings = 'tasks_list'

def get_tasks_list_selector() -> list:
    if tasks_list_settings not in sg.user_settings():
        sg.user_settings_set_entry(tasks_list_settings, list())
    return sg.user_settings_get_entry(tasks_list_settings)

def add_used_task(task_name: str) -> None:
    if task_name not in sg.user_settings_get_entry(tasks_list_settings, list()):
        updated_used_tasks_list = sg.user_settings_get_entry(tasks_list_settings, list())
        updated_used_tasks_list.append(task_name)
        sg.user_settings_set_entry(tasks_list_settings, updated_used_tasks_list)
        
def get_last_window_location(window_title):
    return sg.user_settings_get_entry(last_location_settings_format.format(window_title), (None, None))

def set_last_window_location(window_title, location):
    sg.user_settings_set_entry(last_location_settings_format.format(window_title), location)
