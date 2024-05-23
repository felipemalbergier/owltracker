import subprocess

def clean_linux_window_name(text):
    return text.strip().split(' = ')[-1].replace('"', '').split(',')[0]

def get_active_window_info_linux():
    try:
        # Get the active window ID
        active_window_id = subprocess.check_output(['xprop', '-root', '_NET_ACTIVE_WINDOW']).decode().strip().split()[-1]
        
        # Get the window name
        window_name = subprocess.check_output(['xprop', '-id', active_window_id, 'WM_NAME']).decode().strip().split(' = ')[-1].strip('"')
        
        # Get the window class (application name)
        window_class = subprocess.check_output(['xprop', '-id', active_window_id, 'WM_CLASS']).decode()
        process_name = clean_linux_window_name(window_class)
        
        
        return {"process_name": process_name, "window_title": window_name}
    except:
        # TODO add logger
        pass

if __name__ == "__main__":
    window_info = get_active_window_info_linux()
    if window_info:
        print(f"Active window name: {window_info['window_title']}")
        print(f"Active application name: {window_info['process_name']}")
