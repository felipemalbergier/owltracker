import PySimpleGUI as sg
from owltracker.data.user_settings import get_last_window_location

class View:
    input_task_key = '-INPUT_TASK-'
    stopwatch_button_key = '-STOPWATCH_BUTTON-'
    stopwatch_text_key = '-STOPWATCH-'
    minimize_button_key = '-MINIMIZE_BUTTON-'
    minimized_task_key = '-MINIMIZED_TASK-'
    consider_idle_time = '-IGNORE_TIME_KEY-'
    remove_idle_time = "-SUBTRACT_TIME_KEY-"
    idle_text_key = '-IDLE_TEXT_KEY-'

    def __init__(self):
        self.title_window = "Owltimer"
        self.minimized_title_window = 'minimized'
        self.idle_title_window = 'idle'
        self.size_minimized_window = (170,35)
        self.size_window = (300,300)
        self.start_time_text = 'Start Timer'
        self.stop_time_text = 'Stop'
        self.last_window = None

        self.window = None

    def update_window(self, new_window):
        if self.window:
            if self.last_window:
                self.last_window.close()
            self.last_window = self.window
            self.window.close()
        self.window = new_window

    def create_main_window(self, task=None, task_list=None, stopwatch_active=False):
        size_combo = (int(self.size_window[0] * 0.8),)
        button_text = self.start_time_text if not stopwatch_active else self.stop_time_text
        layout = [
            [sg.Text('TIME', key=self.stopwatch_text_key, font='arial 45', justification='center')],
            [sg.Combo(values=task_list, default_value=task, key=self.input_task_key, font='arial 17', size=size_combo)],
            [sg.Button(button_text, key=self.stopwatch_button_key), sg.Button('Exit')],
            [sg.Button('Minimize', key=self.minimize_button_key)]
        ]
        location = get_last_window_location(self.title_window)
        self.update_window(sg.Window(self.title_window, 
                                     layout, 
                                     size=self.size_window, 
                                     location=location, 
                                     element_justification="center",
                                     finalize=True))

    def create_minimized_window(self, task):
        size_task_name = (self.size_minimized_window[0]//16, self.size_minimized_window[1])
        layout = [[
            sg.Text(task, key=self.minimized_task_key, auto_size_text=True, justification='left', size=size_task_name, tooltip=f" Task: {task}\nDrag to move window "),
            sg.Push(), sg.Text("timer", key=self.stopwatch_text_key, auto_size_text=True, justification='right', enable_events=True, tooltip="Click to go to main window")
        ]]
        location = get_last_window_location(self.minimized_title_window)
        self.update_window(sg.Window(self.minimized_title_window, 
                                     layout, 
                                     size=self.size_minimized_window, 
                                     element_justification="center", 
                                     no_titlebar=True, 
                                     grab_anywhere=True, 
                                     location=location,
                                     alpha_channel=.7,
                                     keep_on_top=True,
                                     finalize=True))

    def create_after_idle_window(self, idle_time=1):
        idle_text = self.create_idle_text(idle_time)
        layout = [[sg.Text(idle_text, key=self.idle_text_key, font="arial 15", justification='center', enable_events=True)],
                [sg.VPush()],
                [sg.Button("Remove idle time", key=self.remove_idle_time),
                sg.Button("Consider idle time", key=self.consider_idle_time)]
        ]
        location = get_last_window_location(self.minimized_title_window)
        self.update_window(sg.Window(self.idle_title_window, layout, size=(300, 200), location=location, element_justification="center", no_titlebar=True, grab_anywhere=True, alpha_channel=.6, keep_on_top=True, finalize=True))

    def create_idle_text(self, idle_time):
        idle_time_string = f'{idle_time//60:.0f} minutes'
        idle_text = f"You were idle for\n{idle_time_string}\nWhat do you want to do?"
        return idle_text

    def change_text_stopwatch_button(self, text):
        self.window[self.stopwatch_button_key].update(text)
        
    def stop_text_stopwatch_button(self):
        self.change_text_stopwatch_button(self.stop_time_text)
        
    def start_text_stopwatch_button(self):
        self.change_text_stopwatch_button(self.start_time_text)
        
    def update_idle_text(self, idle_time):
        self.window[self.idle_text_key].update(self.create_idle_text(idle_time))

