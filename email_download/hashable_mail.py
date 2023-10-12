from imap_tools.message import EmailAddress
from abc import ABC, abstractmethod
import re
from bs4 import BeautifulSoup
from email import message_from_string


class DictCompatible(ABC):
    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass


class HashableEmailAddress(EmailAddress, DictCompatible):
    def __init__(self, value: EmailAddress):
        super().__init__(value.name, value.email)
        self.domain = value.email.split('@')[-1]

    def __hash__(self):
        return hash(self.email)

    def __eq__(self, other):
        if isinstance(other, HashableEmailAddress):
            return self.email == other.email
        return False


def email_address_to_dict(a: HashableEmailAddress, count):
    return {
        "Name": a.name,
        "Email": a.email,
        "Domain": a.domain,
        "Count": count
    }


def extract_unsubscribe_links(email_content: str):

    # Parse the email content
    msg = message_from_string(email_content)

    # Initialize an empty list to store unsubscribe links
    unsubscribe_links = []

    # Extract plain text and HTML bodies
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # skip any text/plain (txt) attachments
            if "attachment" in content_disposition:
                continue
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode()
                unsubscribe_links.extend(re.findall(r'https?://\S+', body))
            elif content_type == "text/html":
                body = part.get_payload(decode=True).decode()
                soup = BeautifulSoup(body, 'html.parser')
                for link in soup.find_all('a', href=True):
                    if "unsubscribe" in link['href'].lower():
                        unsubscribe_links.append(link['href'])
    else:
        # For non-multipart emails
        body = msg.get_payload(decode=True).decode()
        unsubscribe_links.extend(re.findall(r'https?://\S+', body))

    # Return a list of unique unsubscribe links
    return list(set(unsubscribe_links))
