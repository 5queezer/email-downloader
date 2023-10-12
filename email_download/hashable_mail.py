from imap_tools.message import EmailAddress
from abc import ABC, abstractmethod
import re
from bs4 import BeautifulSoup
from imap_tools.message import MailMessage


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
        self.unsubscribe_link = None

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
        "Count": count,
        "Unsubscribe": a.unsubscribe_link
    }


def extract_unsubscribe_links(email_msg: MailMessage) -> str | None:
    def contains_unsubscribe_keyword(text):
        return re.search("unsubscribe|abmelden", text, re.I)

    # Extract from the plain text content
    if hasattr(email_msg, 'text') and email_msg.text:
        for line in email_msg.text.splitlines():
            if contains_unsubscribe_keyword(line):
                potential_links = re.findall(r'https?://\S+', line)
                for link in potential_links:
                    if contains_unsubscribe_keyword(link):
                        return link

    # Extract from the HTML content
    if hasattr(email_msg, 'html') and email_msg.html:
        soup = BeautifulSoup(email_msg.html, 'html.parser')
        for link in soup.find_all('a', href=True):
            if contains_unsubscribe_keyword(link['href']) or contains_unsubscribe_keyword(link.get_text()):
                return link['href']

    # If no unsubscribe links found, return None
    return None
