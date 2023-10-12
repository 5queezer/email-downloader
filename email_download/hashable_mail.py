from imap_tools.message import EmailAddress
from abc import ABC, abstractmethod


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
