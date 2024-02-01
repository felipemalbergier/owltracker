import PySimpleGUI as sg

LAST_LOCATION_SETTINGS_FORMAT = '-LAST_LOCATION_{}-'
TASKS_LIST_SETTINGS = 'tasks_list'
INITIAL_WINDOW_POSITION = (50, 50)

def verify_in_user_settings(user_settings_name) -> bool:
    return user_settings_name in sg.user_settings()


def set_entry_user_settings(key, value) -> None:
    sg.user_settings_set_entry(key, value)


def get_entry_user_settings(key, default_value=None):
    return sg.user_settings_get_entry(key, default=default_value)


def add_used_task(task_name: str) -> None:
    used_tasks_list = get_entry_user_settings(TASKS_LIST_SETTINGS, list())
    if task_name not in used_tasks_list:
        used_tasks_list.append(task_name)
        set_entry_user_settings(TASKS_LIST_SETTINGS, used_tasks_list)


def get_last_window_location(window_title):
    location = get_entry_user_settings(LAST_LOCATION_SETTINGS_FORMAT.format(window_title), INITIAL_WINDOW_POSITION)
    screen_size = sg.Window.get_screen_size()
    return location if location_in_screen_size(location, screen_size) else INITIAL_WINDOW_POSITION


def set_last_window_location(window_title, location):
    set_entry_user_settings(LAST_LOCATION_SETTINGS_FORMAT.format(window_title), location)


def location_in_screen_size(location: tuple, screen_size: tuple) -> bool:
    return 0 < location[0] < screen_size[0] - 10 and 0 < location[1] < screen_size[1] - 10
