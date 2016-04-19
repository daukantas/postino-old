import re
import email.utils

from .compat import unicodify

ADDRESS_REGEX = re.compile(r"^([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)$")

class Address(object):
    def __init__(self, address):
        self.name, self.address = email.utils.parseaddr(unicodify(address))

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, val):
        match = ADDRESS_REGEX.match(val)
        if not match:
            raise ValueError('Invalid address: %s' % val)
        self._address = match.group(0)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val.strip()

    def to_pyzmail(self):
        if self.name:
            return (self.name, self.address)
        else:
            return self.address

    def __str__(self):
        return email.utils.formataddr((self.name or None, self.address))

    def __repr__(self):
        return 'Address("%s")' % str(self)

    def __hash__(self):
        return hash(self.address)

    def __eq__(self, other):
        return self.address == other.address

