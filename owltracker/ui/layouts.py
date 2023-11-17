import PySimpleGUI as sg
from owltracker.data.user_settings import get_last_window_location

input_task_key = '-INPUT_TASK-'
stopwatch_button_key = '-STOPWATCH_BUTTON-'
stopwatch_text_key = '-STOPWATCH-'
minimize_button_key = '-MINIMIZE_BUTTON-'
minimized_task_key = '-MINIMIZED_TASK-'
minimized_stopwatch_text_key = '-MINIMIZED_STOPWATCH-'
ignore_time_key = '-IGNORE_TIME_KEY-'
subtract_time_key = "-SUBTRACT_TIME_KEY-"
idle_text_key = '-IDLE_TEXT_KEY-'
title_window = "Owltimer"
minimized_title_window = 'minimized'
idle_title_window = 'idle'
size_minimized_window = (150,30)
size_window = (300,300)


start_time_text = 'Start Timer'
stop_time_text = 'Stop'


def create_main_window(task=None, task_list=None, stopwatch_active=False):
    size_combo = (int(size_window[0] * 0.8),)
    button_text = start_time_text if not stopwatch_active else stop_time_text
    layout = [
        [sg.Text('TIME', key=stopwatch_text_key, font='arial 45', justification='center')],
        [sg.Combo(values=task_list, default_value=task, key=input_task_key, font='arial 17', size=size_combo)],
        [sg.Button(button_text, key=stopwatch_button_key), sg.Button('Exit')],
        [sg.Button('Minimize', key=minimize_button_key)]
    ]
    location = get_last_window_location(title_window)
    return sg.Window(title_window, 
                    layout, 
                    size=size_window, 
                    location=location,
                    element_justification="center")
    

def create_minimized_window(task):
    size_task_name = (size_minimized_window[0]//16, size_minimized_window[1])
    layout = [[
            sg.Text(task, key=minimized_task_key, auto_size_text=True, justification='left', enable_events=True, size=size_task_name),
            sg.Push(), sg.Text("timer", key=stopwatch_text_key, auto_size_text=True, justification='right', enable_events=True)
    ]]
    location = get_last_window_location(minimized_title_window)
    return sg.Window(minimized_title_window, 
                    layout, 
                    size=size_minimized_window, 
                    element_justification="center", 
                    no_titlebar=True, 
                    grab_anywhere=True,
                    location=location,
                    alpha_channel=.6,
                    keep_on_top=True)


    

def create_after_idle_window(idle_time=1):
    idle_text = create_idle_text(idle_time)
    layout = [[sg.Text(idle_text, key=idle_text_key, font="arial 15", justification='center', enable_events=True)],
            [sg.VPush()],
            [sg.Button("Subtract time", key=subtract_time_key),
            sg.Button("Ignore time", key=ignore_time_key)]
            
    ]
    location = get_last_window_location(minimized_title_window)
    return sg.Window(idle_title_window, 
                    layout, 
                    size=(300, 150), 
                    element_justification="center", 
                    no_titlebar=True, 
                    grab_anywhere=True,
                    location=location,
                    alpha_channel=.6)

    
def create_idle_text(idle_time):
    idle_time_string = f'{idle_time//60:.0f} minutes'
    idle_text = f"You were idle for\n{idle_time_string}\nWhat do you want to do?"
    return idle_text

def change_text_stopwatch_button(window, text):
    window[stopwatch_button_key].update(text)
    
def stop_text_stopwatch_button(window):
    change_text_stopwatch_button(window, stop_time_text)
    
def start_text_stopwatch_button(window):
    change_text_stopwatch_button(window, start_time_text)
    
def update_idle_text(window, idle_time):
    window[idle_text_key].update(create_idle_text(idle_time))
