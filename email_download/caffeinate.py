import sys
import subprocess
from functools import wraps


def is_caffeine_installed():
    try:
        result = subprocess.run(['which', 'caffeine'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        print("Warning: 'which' command not found.")
        return False


def caffeinate_function(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        caffeinate_process = None

        # Start the appropriate command based on the platform
        if sys.platform == "darwin":
            # macOS
            cmd = ['caffeinate', '-i']
        elif sys.platform.startswith("linux"):
            # Only run caffeine if it's installed
            if is_caffeine_installed():
                cmd = ['caffeine']
            else:
                print("Warning: caffeine is not installed on this Linux system.")
                cmd = None
        else:
            cmd = None

        if cmd:
            caffeinate_process = subprocess.Popen(cmd)

        # Execute the wrapped function
        result = func(*args, **kwargs)

        # If caffeinate or caffeine was started, terminate it
        if caffeinate_process:
            caffeinate_process.terminate()

        return result

    return wrapper
