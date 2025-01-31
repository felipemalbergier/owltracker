from owltracker.data.integrations.task import LocalTask
from owltracker.data.integrations.task import Task
from owltracker.data.model import Model
from owltracker.ui.notification import Notification
from owltracker.ui.view import View
from owltracker.utils import WAIT_TIME_MSECONDS
from owltracker.utils import time_to_formated_string
from owltracker.idle_time.idle import get_idle_time
from owltracker.data.user_settings import set_last_window_location
from owltracker.data.activity_tracker.activity_tracker import Activity
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

    def start_stopwatch(self):
        self.stopwatch_active = True
        self.start_time = time.time()
        self.view.stop_text_stopwatch_button()
        self.view.task_notification_start_time = time.time()
        # add_used_task(task_name) # TODO implement it

    def stop_stopwatch(self):
        self.stopwatch_active = False
        time_spent = time.time() - self.start_time
        print(f"Ran for {time_spent} seconds")
        self.model.update_time_integration(time_spent)
        self.view.start_text_stopwatch_button()
        self.view.task_notification_start_time = time.time()

    def handle_stopwatch_event(self, event):
        if self.view.clicked_stop_watch_button(event):
            if not self.stopwatch_active:  # CLICK START TIMER
                self.start_stopwatch()
            else:  # CLiCK STOP TIMER
                self.stop_stopwatch()

    def handle_minimize_event(self, event):
        if self.view.clicked_minimize_button(event):
            self.view.create_minimized_window(self.model.current_task)

    def handle_main_window_event(self, event):
        if self.view.is_minimized_window() and self.view.cliked_go_to_main_window(event):
            self.view.create_main_window(self.model.current_task, self.model.current_tasks, self.stopwatch_active)

    def handle_task_input(self, values):
        if self.view.has_task_input(values):
            input_value = self.view.get_task_input(values)
            if isinstance(input_value, Task):
                self.model.current_task = input_value
            else:
                self.model.current_task = LocalTask(input_value)

    def handle_idle_window_creation(self):
        if self.idle_time > self.notification.LIMIT_IDLE_TIME_WITH_TASK and self.stopwatch_active:
            if not self.view.is_window_idle():
                self.view.create_after_idle_window()
                return True
        return False

    def update_idle_text(self):
        if self.view.is_window_idle():
            self.view.update_idle_text(time.time() - self.idle_start_time)

    def handle_task_notification(self):
        if self.notification.is_quiet_time() or self.view.is_window_idle() or \
            self.idle_time > min(self.notification.LIMIT_IDLE_TIME_WITH_TASK, self.notification.LIMIT_TIME_NO_TASK_SELECTED):
            return
        if not self.stopwatch_active and time.time() - self.notification.task_notification_start_time > self.notification.LIMIT_TIME_NO_TASK_SELECTED:
            self.notification.notify_not_working_task()
        if self.stopwatch_active and time.time() - self.notification.task_notification_start_time > self.notification.LIMIT_TIME_WITH_TASK_SELECTED:
            self.notification.notify_working_same_task(self.model.current_task.title)

    def handle_idle_screen_actions(self, event):
        if self.view.clicked_consider_idle_time(event) or self.view.clicked_remove_idle_time(event):
            self.view.create_minimized_window(task=self.model.current_task)
            self.notification.task_notification_start_time = time.time()
            if self.view.clicked_remove_idle_time(event):
                self.start_time += time.time() - self.idle_start_time

    def run(self):
        self.view.create_main_window(self.model.current_task, self.model.current_tasks, self.stopwatch_active)
        while True:
            event, values = self.view.window.read(timeout=WAIT_TIME_MSECONDS)
            if self.view.clicked_close(event):
                break
            print(event, values)
            self.handle_stopwatch_event(event)
            if event == '__TIMEOUT__' and self.stopwatch_active and not self.view.is_window_idle():
                self.view.update_timer(self.start_time)
            self.handle_minimize_event(event)
            self.handle_main_window_event(event)

            self.idle_time = get_idle_time()

            if self.idle_time < 1 and not self.view.is_window_idle():
                self.idle_start_time = time.time() - self.idle_time
            if self.handle_idle_window_creation():
                continue  # need to 'read' again to refresh the window

            self.update_idle_text()
            self.view.make_window_reachable()
            set_last_window_location(self.view.window.Title, self.view.window.current_location())
            self.handle_task_input(values)
            self.handle_task_notification()
            self.handle_idle_screen_actions(event)
            if self.idle_time < 1 and self.view.window.Title != self.view.idle_title_window:
                self.activity.log_activity(event=event)
            print(datetime.now(), "idle", self.idle_time, "time task:", time_to_formated_string(time.time() - self.start_time))
        self.view.window.close()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
