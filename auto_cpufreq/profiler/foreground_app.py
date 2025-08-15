import subprocess
import shutil
import psutil

def get_foreground_app_pid():
    """
    Gets the PID of the foreground application using xdotool.
    Returns the PID as an integer, or None if not found or xdotool is not installed.
    """
    if not shutil.which("xdotool"):
        return None

    try:
        # Get window ID of active window
        active_window_cmd = ["xdotool", "getactivewindow"]
        window_id = subprocess.check_output(active_window_cmd, text=True).strip()

        # Get PID from window ID
        pid_cmd = ["xdotool", "getwindowpid", window_id]
        pid = subprocess.check_output(pid_cmd, text=True).strip()
        return int(pid)
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return None

def get_process_name_by_pid(pid):
    """
    Gets the process name for a given PID.
    Returns the process name as a string, or None if not found.
    """
    if pid is None:
        return None
    try:
        process = psutil.Process(pid)
        return process.name()
    except psutil.NoSuchProcess:
        return None

def get_foreground_app():
    """
    Gets the process name of the foreground application.
    """
    pid = get_foreground_app_pid()
    return get_process_name_by_pid(pid)


if __name__ == '__main__':
    app_name = get_foreground_app()
    if app_name:
        print(f"Foreground application: {app_name}")
    else:
        print("Could not determine foreground application.")
