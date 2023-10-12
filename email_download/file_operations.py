import os
import shutil
import click


def clear_directory(directory):
    """Clears all files and subdirectories in the specified directory."""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)


def manage_directory(directory, delete_contents):
    if os.path.exists(directory) and os.listdir(directory):
        if delete_contents or click.confirm(f"'{directory}' is not empty. Do you want to delete its contents?",
                                            default=False):
            clear_directory(directory)
    elif not os.path.exists(directory):
        os.makedirs(directory)
