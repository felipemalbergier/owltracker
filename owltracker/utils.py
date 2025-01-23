WAIT_TIME_MSECONDS = 100

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

def location_in_screen_size(location: tuple, screen_size: tuple) -> bool:
    return 0 < location[0] < screen_size[0] - 10 and 0 < location[1] < screen_size[1] - 10
    