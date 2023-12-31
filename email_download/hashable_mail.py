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
    _unsubscribe_link: str
    _to: tuple

    @property
    def unsubscribe_link(self) -> str:
        return self._unsubscribe_link

    @unsubscribe_link.setter
    def unsubscribe_link(self, value: str):
        self._unsubscribe_link = value

    @property
    def to(self) -> str:
        return ','.join(self._to) if self._to else ''

    @to.setter
    def to(self, value: tuple | str):
        if isinstance(value, str):
            self._to = tuple(value)
        else:
            self._to = value

    def __init__(self, value: EmailAddress, to: tuple = None):
        super().__init__(value.name, value.email)
        self.domain = value.email.split('@')[-1]
        self.to = to

    def __hash__(self):
        return hash(self.email)

    def __eq__(self, other):
        if isinstance(other, HashableEmailAddress):
            return self.email == other.email
        return False


def email_address_to_dict(a: HashableEmailAddress, count):
    return {
        "Name": a.name,
        "From": a.email,
        "To": a.to,
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
