import sys

PYTHON_VERSION = sys.version_info[0]

PY2 = PYTHON_VERSION == 2
PY3 = PYTHON_VERSION == 3


if PY2:
    def unicodearg(s):
        return s.decode(sys.stdin.encoding)
elif PY3:
    def unicodearg(s):
        assert(isinstance(s, str))
        return s

if PY2:
    UNICODE_TYPE = unicode
    BASESTRING_TYPE = basestring
elif PY3:
    UNICODE_TYPE = str
    BASESTRING_TYPE = str


def unicodify(s):
    return UNICODE_TYPE(s)


def isunicode(s):
    return isinstance(s, UNICODE_TYPE)


def isbasestring(s):
    return isinstance(s, BASESTRING_TYPE)


if PY2:
    import codecs
    def load_file(filename, encoding):
        reader = codecs.getreader(encoding)
        if filename == '-':
            return reader(sys.stdin).read()
        else:
            with open(filename, 'r') as f:
                return reader(codecs.getreader())
elif PY3:
    import io
    def load_file(filename, encoding):
        if filename == '-':
            return io.TextIOWrapper(sys.stdin.buffer, encoding=encoding).read()
        else:
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()

