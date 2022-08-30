from owltracker.utils import save_time, time_to_formated_string
from owltracker.idle import get_idle_time

import PySimpleGUI as sg
from plyer import notification

import time

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
last_location_key_format = '-LAST_LOCATION_{}-'
size_minimized_window = (150,30)

start_time_text = 'Start Timer'
stop_time_text = 'Stop'


limit_idle_time_with_task = 15 * 60  # in seconds
limit_time_no_task_selected = 15 * 60  # in seconds
limit_time_with_task_selected = 30 * 60 # in seconds

stopwatch_active = False
idle_start_time = 0
start_time = 0
task_notification_start_time = time.time()
idle_time = 0
task_name = ''


def create_idle_text(idle_time):
    idle_time_string = f'{idle_time//60:.0f} minutes'
    idle_text = f"You were idle for\n{idle_time_string}\nWhat do you want to do?"
    return idle_text


def create_minimized_window(task_name):
    size_task_name = (size_minimized_window[0]//16, size_minimized_window[1])
    layout = [[
            sg.Text(task_name, key=minimized_task_key, justification='left', enable_events=True, size=size_task_name),
            sg.Push(), sg.Text("timer", key=stopwatch_text_key, justification='right', enable_events=True)
    ]]
    location = sg.user_settings_get_entry(last_location_key_format.format(minimized_title_window), (None, None))
    return sg.Window(minimized_title_window, 
                    layout, 
                    size=size_minimized_window, 
                    element_justification="center", 
                    no_titlebar=True, 
                    grab_anywhere=True,
                    location=location,
                    alpha_channel=.6)
    

def create_after_idle_window(idle_time=1):
    idle_text = create_idle_text(idle_time)
    layout = [[sg.Text(idle_text, key=idle_text_key, font="arial 15", justification='center', enable_events=True)],
            [sg.VPush()],
            [sg.Button("Subtract time", key=subtract_time_key),
            sg.Button("Ignore time", key=ignore_time_key)]
            
    ]
    location = sg.user_settings_get_entry(last_location_key_format.format(minimized_title_window), (None, None))
    return sg.Window(idle_title_window, 
                    layout, 
                    size=(300, 150), 
                    element_justification="center", 
                    no_titlebar=True, 
                    grab_anywhere=True,
                    location=location,
                    alpha_channel=.6)
    
def create_window(task_name=''):
    layout = [ 
        [sg.Text('TIME', key=stopwatch_text_key, font='arial 45', justification='center')],
        [sg.Input(task_name, key=input_task_key, justification='center', font='arial 23')],
        [sg.Button(start_time_text, key=stopwatch_button_key), sg.Button('Exit')],
        [sg.Button('Minimize', key=minimize_button_key, visible=False)]
    ]
    location = sg.user_settings_get_entry(last_location_key_format.format(title_window), (None, None))
    return sg.Window(title_window, 
                    layout, 
                    size=(300,300), 
                    location=location,
                    element_justification="center")


window = create_window()
# window = create_after_idle_window(15 * 60)
    
while True:
    event, values = window.read(timeout=100)   # Read the event that happened and the values dictionary

    if event == sg.WIN_CLOSED or event == 'Exit':     # If user closed window with X or if user clicked "Exit" button then exit
        break
    print(event, values)
    if event == 'Button':
        print('You pressed the button')
        print(values)
        print(event)
    
    if event == stopwatch_button_key:
        if not stopwatch_active:
            stopwatch_active = True
            start_time = time.time()
            window[stopwatch_button_key].update(stop_time_text)
            task_notification_start_time = time.time()
        else:
            stopwatch_active = False
            time_spent = time.time() - start_time
            print(f"Ran for {time_spent} seconds")
            save_time(values[input_task_key], time_spent)
            window[stopwatch_button_key].update(start_time_text)
            task_notification_start_time = time.time()
    
    if event == '__TIMEOUT__' and stopwatch_active and window.Title != idle_title_window:
        elapsed_time = time_to_formated_string(time.time() - start_time)
        window[stopwatch_text_key].update(elapsed_time)
        
        if minimize_button_key in [e.key for e in window.element_list()]:
            window[minimize_button_key].update(visible=True)

    if event == minimize_button_key:
        window.close()
        window = create_minimized_window(task_name=values[input_task_key])
        continue # need to 'read' again to execute code
    
    if window.Title == minimized_title_window and event in [minimized_task_key, stopwatch_text_key]:
        window.close()
        window = create_window(task_name=window[minimized_task_key].DisplayText)
        continue # need to 'read' again to execute code
    
    idle_time = get_idle_time()
    if idle_time > limit_idle_time_with_task and stopwatch_active:
        if window.Title != idle_title_window:
            window.close()
            window = create_after_idle_window()
            idle_start_time = time.time() - idle_time
            continue # need to 'read' again to execute code
        else:
            window[idle_text_key].update(create_idle_text(idle_time))
        
    sg.user_settings_set_entry(last_location_key_format.format(window.Title), window.current_location())
    
    if input_task_key in values:
        task_name = values[input_task_key]
    
    if not task_name and time.time() - task_notification_start_time > limit_time_no_task_selected:
        notification.notify(
        title='Are you working on a task?',
        message="Don't forget to add to Owlltracker",
        app_name='Owltracker',
        timeout=5,
        # app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
        )
        task_notification_start_time = time.time()
    
    if task_name and time.time() - task_notification_start_time > limit_time_with_task_selected:
        notification.notify(
        title=f'Still working on {task_name}',
        message="Don't forget to update on Owlltracker",
        app_name='Owltracker',
        timeout=5,
        # app_icon='path/to/the/icon.' + ('ico' if platform == 'win' else 'png')
        )
        task_notification_start_time = time.time()
    
    
    if event == ignore_time_key:
        window.close()
        window = create_minimized_window(task_name)
        task_notification_start_time = time.time()
        idle_time = 0
    if event == subtract_time_key:
        start_time += time.time() - idle_start_time
        window.close()
        window = create_minimized_window(task_name)
        task_notification_start_time = time.time()
        idle_time = 0
    print("idle", idle_time)
window.close()
