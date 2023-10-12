#!/usr/bin/env python3

import os
import hashlib
import sys

from tqdm import tqdm
from imap_tools import MailBox
import click
import shutil
from operator import attrgetter
from hashable_mail import HashableEmailAddress


@click.command()
@click.option('--host', prompt='IMAP Host', help='The IMAP server host.')
@click.option('--user', prompt='Username', help='The IMAP server username/email.')
@click.option('--password', prompt='Password', hide_input=True, help='The IMAP server password.')
@click.option('--directory', default="saved_emails", prompt='Save Directory',
              help='Directory to save downloaded emails.')
@click.option('--delete-contents', default=False, help='Delete the contents in the save directory..')
@click.option('--overwrite', default=True, help='Overwrite the files in the save directory.')
def main(host, user, password, directory, delete_contents, overwrite):
    """Download emails from the specified IMAP server and save them to the given directory."""

    def clear_directory(directory):
        """Clears all files and subdirectories in the specified directory."""
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)

    def clean_subject(subject):
        return subject.replace("/", "_").replace("\\", "_").replace(":", "_").replace("\0", "_")

    def generate_filename(msg):
        truncated_subject = clean_subject(msg.subject)
        hash_object = hashlib.sha1(msg.subject.encode())
        hex_dig = hash_object.hexdigest()[:6]
        max_subject_length = 255 - len(hex_dig) - len(".eml") - 1
        truncated_subject = truncated_subject[:max_subject_length]
        filename = f"{truncated_subject}_{hex_dig}.eml"
        return filename

    if os.path.exists(directory) and os.listdir(directory):  # Checking if directory is not empty
        if delete_contents or click.confirm(f"'{directory}' is not empty. Do you want to delete its contents?",
                                            default=False):
            clear_directory(directory)
    elif not os.path.exists(directory):
        os.makedirs(directory)

    senders = dict()

    with MailBox(host).login(user, password) as mailbox:
        total_emails = len(mailbox.numbers())
        with tqdm(total=total_emails, dynamic_ncols=True) as pbar:
            for msg in mailbox.fetch():
                email_address = HashableEmailAddress(msg.from_values)
                senders[email_address] = senders.get(email_address, 0) + 1

                formatted_from = f"{msg.from_values.full[:30]:<30}"
                formatted_subject = f"{msg.subject[:40]:<40}"

                pbar.set_description(f"From: {formatted_from} | Subject: {formatted_subject}")

                filepath = os.path.join(directory, generate_filename(msg))

                if overwrite:
                    with open(filepath, 'wb') as file:
                        try:
                            email_object = msg.obj.as_string().encode('utf-8')
                            file.write(email_object)
                        except UnicodeError:
                            print(f'\nSkipping {msg.from_values.full} {msg.subject}', file=sys.stderr)

                    email_timestamp = msg.date.timestamp()
                    os.utime(filepath, (email_timestamp, email_timestamp))

                pbar.update(1)

    with open(os.path.join(directory, 'senders.txt'), 'w') as file:
        for sender in sorted(senders, key=attrgetter('domain')):
            email = sender.email
            name = sender.name
            domain = sender.domain
            count = senders[sender]
            print(email, name, domain, count, file=file, sep=";")


if __name__ == "__main__":
    main()
