from owltracker.data.model import Model
from owltracker.ui.notification import Notification
from owltracker.utils import time_to_formated_string
from owltracker.idle import get_idle_time
from owltracker.ui.layouts import input_task_key
from owltracker.ui.layouts import start_text_stopwatch_button
from owltracker.ui.layouts import stop_text_stopwatch_button
from owltracker.ui.layouts import update_idle_text
from owltracker.ui.layouts import update_list_tasks
from owltracker.ui.layouts import stopwatch_button_key
from owltracker.ui.layouts import stopwatch_text_key
from owltracker.ui.layouts import minimize_button_key
from owltracker.ui.layouts import minimized_task_key
from owltracker.ui.layouts import ignore_time_key
from owltracker.ui.layouts import subtract_time_key
from owltracker.ui.layouts import minimized_title_window
from owltracker.ui.layouts import idle_title_window
from owltracker.ui.layouts import create_window
from owltracker.ui.layouts import create_minimized_window
from owltracker.ui.layouts import create_after_idle_window
from owltracker.ui.notification import limit_idle_time_with_task
from owltracker.ui.notification import limit_time_no_task_selected
from owltracker.ui.notification import limit_time_with_task_selected
from owltracker.data.user_settings import set_last_window_location
from owltracker.data.user_settings import add_used_task

import PySimpleGUI as sg

import time


class Controller:
    def __init__(self) -> None:
        self.notification = Notification()
        self.model = Model()
        self.stopwatch_active = False
        self.idle_start_time = 0
        self.start_time = 0
        self.idle_time = 0
        self.task_name = ''

    def initialize(self):
        window = create_window()
        window.read(timeout=100)
        list_tasks = self.model.get_tasks_list_selector()
        update_list_tasks(window, list_tasks)
        return window
        

    def run(self):
        window = self.initialize()
        while True:
            event, values = window.read(timeout=100)
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            print(event, values)
            
            if event == stopwatch_button_key:
                if not self.stopwatch_active: # CLICK START TIMER
                    self.stopwatch_active = True
                    self.start_time = time.time()
                    stop_text_stopwatch_button(window)
                    task_notification_start_time = time.time() # move to view
                    # add_used_task(task_name) # TODO implement it
                else:                    # CLiCK STOP TIMER
                    self.stopwatch_active = False
                    time_spent = time.time() - self.start_time
                    print(f"Ran for {time_spent} seconds")
                    self.model.save_time(values[input_task_key], time_spent) # move to model
                    start_text_stopwatch_button(window)
                    task_notification_start_time = time.time() # move to view
            
            # Update timer
            if event == '__TIMEOUT__' and self.stopwatch_active and window.Title != idle_title_window:
                elapsed_time = time_to_formated_string(time.time() - self.start_time) # to view
                window[stopwatch_text_key].update(elapsed_time) # to view
                
                # make sure minimize button is active because it only appear
                print("should visible minimeze?")
                # if minimize_button_key in [e.key for e in window.element_list()]:
                #     window[minimize_button_key].update(visible=True)

            # Click to Minimize window
            if event == minimize_button_key:
                window.close()
                window = create_minimized_window(task=values[input_task_key])
                continue # need to 'read' again to execute code
            
            # Click minimized window to go to main screen
            if window.Title == minimized_title_window and event in [minimized_task_key, stopwatch_text_key]:
                window.close()
                window = create_window(task=values[input_task_key], stop_watch_active=self.stopwatch_active)
                continue # need to 'read' again to execute code
            
            # Create idle window to verify idle time
            self.idle_time = get_idle_time()
            if self.idle_time > limit_idle_time_with_task and self.stopwatch_active:
                if window.Title != idle_title_window:
                    window.close()
                    window = create_after_idle_window()
                    self.idle_start_time = time.time() - self.idle_time
                    continue # need to 'read' again to execute code
                else:
                    update_idle_text(window, self.idle_time)
            
            set_last_window_location(window.Title, window.current_location())
            
            if input_task_key in values:
                self.task_name = values[input_task_key]
            
            # notify if not working on task for more than X seconds
            if not self.stopwatch_active and time.time() - self.notification.task_notification_start_time > limit_time_no_task_selected:
                self.notification.notify_not_working_task()
            
            # notify if working on task for more than Y seconds
            if self.stopwatch_active and time.time() - self.notification.task_notification_start_time > limit_time_with_task_selected:
                self.notification.notify_working_same_task(self.task_name)
            
            # Actions for idle screen
            if event == ignore_time_key:
                window.close()
                window = create_minimized_window(self.task_name)
                self.notification.task_notification_start_time = time.time()
                self.idle_time = 0
            if event == subtract_time_key:
                self.start_time += time.time() - self.idle_start_time
                window.close()
                window = create_minimized_window(self.task_name)
                self.notification.task_notification_start_time = time.time()
                self.idle_time = 0
            print("idle", self.idle_time)
        window.close()
        
        
if __name__ == "__main__":
    controller = Controller()
    controller.run()