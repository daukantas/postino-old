import os.path
from ConfigParser import RawConfigParser

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
    'name': 'Postino',
    'to': None,
    'mode': 'normal',
    'port': 25,
}

class Config(object):
    def __init__(self, server, port,
                 user, password,
                 name=None,
                 mode=None, to=None):
        self.server = server
        self.port = port
        self.user = user
        self.password = password
        self.mode = mode
        self.to = to
        self.name = name

    @classmethod
    def load(cls, filename):
        cfg = RawConfigParser(defaults=DEFAULTS)
        cfg.read(filename)

        return cls(
            cfg.get('postino', 'server'), cfg.getint('postino', 'port'),
            cfg.get('postino', 'user'), cfg.get('postino', 'password'),
            cfg.get('postino', 'name'), cfg.get('postino', 'mode'),
            cfg.get('postino', 'to'))

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

