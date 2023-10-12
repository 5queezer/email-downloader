import hashlib
import os
import shutil
import click
from imap_tools import MailMessage
import sys


def clear_directory(directory: str):
    """Clears all files and subdirectories in the specified directory."""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)


def manage_directory(directory: str, delete_contents: bool):
    if os.path.exists(directory) and os.listdir(directory):
        if delete_contents or click.confirm(f"'{directory}' is not empty. Do you want to delete its contents?",
                                            default=False):
            clear_directory(directory)
    elif not os.path.exists(directory):
        os.makedirs(directory)


def generate_filename(msg: MailMessage):
    def clean_subject(subject):
        return subject.replace("/", "_").replace("\\", "_").replace(":", "_").replace("\0", "_")

    truncated_subject = clean_subject(msg.subject)
    hash_object = hashlib.sha1(msg.subject.encode())
    hex_dig = hash_object.hexdigest()[:6]
    max_subject_length = 255 - len(hex_dig) - len(".eml") - 1
    truncated_subject = truncated_subject[:max_subject_length]
    filename = f"{truncated_subject}_{hex_dig}.eml"
    return filename


def save_mail(directory: str, msg: MailMessage):
    filepath = os.path.join(directory, generate_filename(msg))

    with open(filepath, 'wb') as file:
        try:
            email_object = msg.obj.as_string().encode('utf-8')
            file.write(email_object)
        except UnicodeError:
            print(f'\nSkipping {msg.from_values.full} {msg.subject}', file=sys.stderr)

    email_timestamp = msg.date.timestamp()
    os.utime(filepath, (email_timestamp, email_timestamp))
