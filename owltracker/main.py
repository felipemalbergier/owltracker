from owltracker.utils import save_time, time_to_formated_string
from owltracker.idle import get_idle_time
from owltracker.ui.layouts import input_task_key
from owltracker.ui.layouts import stopwatch_button_key
from owltracker.ui.layouts import stopwatch_text_key
from owltracker.ui.layouts import minimize_button_key
from owltracker.ui.layouts import minimized_task_key
from owltracker.ui.layouts import minimized_stopwatch_text_key
from owltracker.ui.layouts import ignore_time_key
from owltracker.ui.layouts import subtract_time_key
from owltracker.ui.layouts import idle_text_key
from owltracker.ui.layouts import title_window
from owltracker.ui.layouts import minimized_title_window
from owltracker.ui.layouts import idle_title_window
from owltracker.ui.layouts import size_minimized_window
from owltracker.ui.layouts import create_window
from owltracker.ui.layouts import create_minimized_window
from owltracker.ui.layouts import create_after_idle_window
from owltracker.ui.layouts import create_idle_text
from owltracker.ui.layouts import start_time_text
from owltracker.ui.layouts import stop_time_text
from owltracker.data.user_settings import set_last_window_location
from owltracker.data.user_settings import add_used_task

import PySimpleGUI as sg
from plyer import notification

import time

limit_idle_time_with_task = 15 * 60  # in seconds
limit_time_no_task_selected = 15 * 60  # in seconds
limit_time_with_task_selected = 30 * 60 # in seconds

stopwatch_active = False
idle_start_time = 0
start_time = 0
task_notification_start_time = time.time()
idle_time = 0
task_name = ''



window = create_window()
# window = create_after_idle_window(15 * 60)
    
while True:
    event, values = window.read(timeout=100)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    print(event, values)
    
    if event == stopwatch_button_key:
        if not stopwatch_active: # CLICK START TIMER
            stopwatch_active = True
            start_time = time.time()
            window[stopwatch_button_key].update(stop_time_text) # move to view
            task_notification_start_time = time.time() # move to view
            # add_used_task(task_name) # TODO implement it
        else:                    # CLiCK STOP TIMER
            stopwatch_active = False
            time_spent = time.time() - start_time
            print(f"Ran for {time_spent} seconds")
            save_time(values[input_task_key], time_spent) # move to model
            window[stopwatch_button_key].update(start_time_text) # move to view
            task_notification_start_time = time.time() # move to view
    
    # Update timer
    if event == '__TIMEOUT__' and stopwatch_active and window.Title != idle_title_window:
        elapsed_time = time_to_formated_string(time.time() - start_time) # to view
        window[stopwatch_text_key].update(elapsed_time) # to view
        
        # make sure minimize button is active because it only appear
        print("should visible minimeze?")
        # if minimize_button_key in [e.key for e in window.element_list()]:
        #     window[minimize_button_key].update(visible=True)

    # Click to Minimize window
    if event == minimize_button_key:
        window.close()
        window = create_minimized_window(task_name=values[input_task_key])
        continue # need to 'read' again to execute code
    
    # Click minimized window to go to main screen
    if window.Title == minimized_title_window and event in [minimized_task_key, stopwatch_text_key]:
        window.close()
        window = create_window(task_name=window[minimized_task_key].DisplayText)
        continue # need to 'read' again to execute code
    
    # Create idle window to verify idle time
    idle_time = get_idle_time()
    if idle_time > limit_idle_time_with_task and stopwatch_active:
        if window.Title != idle_title_window:
            window.close()
            window = create_after_idle_window()
            idle_start_time = time.time() - idle_time
            continue # need to 'read' again to execute code
        else:
            window[idle_text_key].update(create_idle_text(idle_time))
    
    set_last_window_location(window.Title, window.current_location())
    
    if input_task_key in values:
        task_name = values[input_task_key]
    
    # notify if not working on task for more than X seconds
    if not stopwatch_active and time.time() - task_notification_start_time > limit_time_no_task_selected:
        notification.notify(
        title='Are you working on a task?',
        message="Don't forget to add to Owlltracker",
        app_name='Owltracker',
        timeout=5,
        )
        task_notification_start_time = time.time()
    
    # notify if working on task for more than Y seconds
    if stopwatch_active and time.time() - task_notification_start_time > limit_time_with_task_selected:
        notification.notify(
        title=f'Still working on {task_name}',
        message="Don't forget to update on Owlltracker",
        app_name='Owltracker',
        timeout=5,
        )
        task_notification_start_time = time.time()
    
    # Actions for idle screen
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
