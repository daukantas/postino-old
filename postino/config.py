import os.path

try:
    from ConfigParser import RawConfigParser
except ImportError:
    from configparser import RawConfigParser

from .address import Address

# paths to default configuration files
DEFAULT_CONFIG_PATHS = [
    # current directory
    'postino.ini',
    # home directory
    os.path.expanduser('~/.postino.ini'),
    # /etc directory
    '/etc/postino.ini',
]

DEFAULTS = {
    'sender': u'Postino <postino@postino.com>',
    'to': None,
    'cc': None,
    'bcc': None,
    'mode': 'normal',
    'port': 25,
    'subject': u'Postino',
}

class Config(object):
    def __init__(self, server, port,
                 login, password,
                 sender=None,
                 mode=None, to=None,
                 cc=None, bcc=None,
                 subject=None):
        self.server = server
        self.port = port
        self.login = login
        self.password = password
        self.mode = mode
        self.to = Address(to) if to else None
        self.cc = Address(cc) if cc else None
        self.bcc = Address(bcc) if bcc else None
        self.sender = Address(sender)
        self.subject = subject

    @classmethod
    def load(cls, filename):
        cfg = RawConfigParser(defaults=DEFAULTS)
        cfg.read(filename)

        return cls(
            cfg.get('postino', 'server'), cfg.getint('postino', 'port'),
            cfg.get('postino', 'login'), cfg.get('postino', 'password'),
            cfg.get('postino', 'sender'), cfg.get('postino', 'mode'),
            cfg.get('postino', 'to'), cfg.get('postino', 'cc'),
            cfg.get('postino', 'bcc'), cfg.get('postino', 'subject'))

    @classmethod
    def load_any(cls, filenames):
        for filename in filenames:
            try:
                return cls.load(filename)
            except Exception as e:
                print(e)
        return None

    @classmethod
    def load_default(cls):
        return cls.load_any(DEFAULT_CONFIG_PATHS)

