from owltracker.data.integrations.task import LocalTask
from owltracker.data.integrations.task import Task
from owltracker.data.model import Model
from owltracker.ui.notification import Notification
from owltracker.ui.view import View
from owltracker.utils import WAIT_TIME_MSECONDS
from owltracker.utils import time_to_formated_string
from owltracker.idle_time.idle import get_idle_time
from owltracker.data.user_settings import set_last_window_location
from owltracker.data.user_settings import add_used_task
from owltracker.data.activity_tracker.activity_tracker import Activity

import PySimpleGUI as sg

import time
from datetime import datetime

class Controller:
    def __init__(self) -> None:
        self.notification = Notification()
        self.model = Model()
        self.activity = Activity()
        self.view = View()
        
        self.stopwatch_active = False
        self.idle_start_time = 0
        self.start_time = 0
        self.idle_time = 0

    def run(self):
        self.view.create_main_window(self.model.current_task, self.model.current_tasks, self.stopwatch_active)
        while True:
            event, values = self.view.window.read(timeout=WAIT_TIME_MSECONDS)
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            print(event, values)
            
            if event == self.view.stopwatch_button_key:
                if not self.stopwatch_active: # CLICK START TIMER
                    self.stopwatch_active = True
                    self.start_time = time.time()
                    self.view.stop_text_stopwatch_button()
                    self.view.task_notification_start_time = time.time()
                    # add_used_task(task_name) # TODO implement it
                else:                    # CLiCK STOP TIMER
                    self.stopwatch_active = False
                    time_spent = time.time() - self.start_timer_time
                    print(f"Ran for {time_spent} seconds")
                    self.model.update_time_integration(time_spent)
                    self.view.start_text_stopwatch_button()
                    self.view.task_notification_start_time = time.time()
            
            # Update timer
            if event == '__TIMEOUT__' and self.stopwatch_active and self.view.window.Title != self.view.idle_title_window:
                elapsed_time = time_to_formated_string(time.time() - self.start_time) # to view
                self.view.window[self.view.stopwatch_text_key].update(elapsed_time) # to view

            # Click to Minimize window
            if event == self.view.minimize_button_key:
                self.view.window.close()
                self.view.create_minimized_window(task=self.model.current_task)
                continue # need to 'read' again to execute code
            
            # Click to go to main Window
            if self.view.window.Title == self.view.minimized_title_window:
                if event == self.view.stopwatch_text_key:
                    self.view.window.close()
                    self.view.create_main_window(self.model.current_task, self.model.current_tasks, self.stopwatch_active)
                    continue # need to 'read' again to execute code

            # Create idle window to verify idle time
            self.idle_time = get_idle_time()
            self.idle_start_time = time.time() - self.idle_time
            if self.idle_time > self.notification.LIMIT_IDLE_TIME_WITH_TASK and self.stopwatch_active:
                if self.view.window.Title != self.view.idle_title_window:
                    self.view.window.close()
                    self.view.create_after_idle_window()
                    continue # need to 'read' again to execute code
                else:
                    self.view.update_idle_text(time.time() - self.idle_start_time)
            
            set_last_window_location(self.view.window.Title, self.view.window.current_location())
            
            if self.view.input_task_key in values:
                input_value = values[self.view.input_task_key]
                if isinstance(input_value, Task):
                    self.model.current_task = values[self.view.input_task_key]
                else:
                    self.model.current_task = LocalTask(input_value)
            
            # notify if not working on task for more than X seconds
            if not self.stopwatch_active and time.time() - self.notification.task_notification_start_time > self.notification.LIMIT_TIME_NO_TASK_SELECTED:
                self.notification.notify_not_working_task()
            
            # notify if working on task for more than Y seconds
            if self.stopwatch_active and time.time() - self.notification.task_notification_start_time > self.notification.LIMIT_TIME_WITH_TASK_SELECTED:
                self.notification.notify_working_same_task(self.model.current_task.title)
            
            # Actions for idle screen
            if event == self.view.consider_idle_time:
                self.view.create_minimized_window(task=self.model.current_task)
                self.notification.task_notification_start_time = time.time()
                self.idle_time = 0
            if event == self.view.remove_idle_time:
                self.start_time += time.time() - self.idle_start_time
                self.view.create_minimized_window(task=self.model.current_task)
                self.notification.task_notification_start_time = time.time()
                self.idle_time = 0

            # not log activity when idle > 1 second or in idle screen 
            if self.idle_time < 1 and self.view.window.Title != self.view.idle_title_window:
            #     if self.idle_start_time 
                # recognize if click button to ignore time 
                # i can add information to activity table, just of 
                # since we are clicking information on the screen we might add a new row on the table and add that info 
                # if they choose to 
                self.activity.log_activity(event=event)
            
            print(datetime.now(), "idle", self.idle_time)
        
        self.view.window.close()
        
        
if __name__ == "__main__":
    controller = Controller()
    controller.run()