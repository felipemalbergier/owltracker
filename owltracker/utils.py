from datetime import datetime
import os
from time import time
from owltracker.data.user_settings import update_time_integration

times_file = os.path.join(os.path.dirname(__file__), "time_database.csv") 
columns_times_file = ['Time Input', 'Task Name', 'Time Spent']

def save_time(task_name: str, time: int):
    if not os.path.exists(times_file):
        with open(times_file, 'w') as f:
            f.write(";".join(columns_times_file))
            f.write("\n")

    now = datetime.now().isoformat()
    with open(times_file, 'a') as f:
        f.write(";".join([now, task_name, f"{time:.0f}"]))
        f.write("\n")
    
    update_time_integration(task_name, time)


def time_to_formated_string(time_time: float):
    hours = int(time_time / (60 * 60))
    minutes = int((time_time - hours * (60 * 60))/ 60)
    
    hours = str(hours).rjust(2, '0')
    minutes = str(minutes).rjust(2, '0')
    
    seconds = str(int(time_time % 60)).rjust(2, '0')
    
    if hours != "00":
        return f"{hours}:{minutes}:{seconds}"
    elif minutes != "00":
        return f"{minutes}:{seconds}"
    else:
        return f'{time_time % 60:.1f}'

