import json
import os.path


# paths to default configuration files
DEFAULT_CONFIG_PATHS = [
    # current directory
    'postino.json',
    # home directory
    os.path.expanduser('~/.postino.json'),
    # /etc directory
    '/etc/postino.json',
]


class Config(object):
    def __init__(self, server, port,
                 user, password,
                 name=None,
                 mode=None, to=None):
        self.server = server
        self.port = port or 25
        self.user = user
        self.password = password
        self.mode = mode or 'normal'
        self.to = to
        self.name = name or 'Postino'

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as fileobj:
            cfg = json.loads(fileobj.read())

        return cls(cfg['server'], cfg['port'],
                   cfg['user'], cfg['password'],
                   cfg.get('name'),
                   cfg.get('mode'),
                   cfg.get('to'))

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

