#!/usr/bin/env python3
import csv

from tqdm import tqdm
from imap_tools import MailBox
import click

from hashable_mail import HashableEmailAddress, email_address_to_dict, extract_unsubscribe_links
from file_operations import manage_directory, save_mail


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

    manage_directory(directory, delete_contents)

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
                unsubscribe_link = extract_unsubscribe_links(msg)

                if overwrite:
                    save_mail(directory, msg)

                pbar.update(1)

    with open('email_addresses.csv', 'w', newline='') as file:
        # Obtain headers dynamically
        sample_key = next(iter(senders), None)  # Get the first key from the senders dictionary
        headers = list(email_address_to_dict(sample_key, 0).keys()) if sample_key else []

        writer = csv.DictWriter(file, fieldnames=headers, delimiter=';')
        writer.writeheader()  # Writes the headers

        for address, count in senders.items():
            writer.writerow(email_address_to_dict(address, count))


if __name__ == "__main__":
    main()
