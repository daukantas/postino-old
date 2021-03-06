#!/usr/bin/env python


from markdown import markdown
from pyzmail import compose_mail, send_mail

from . import config
from . import compat
from .address import Address


class PostinoError(Exception):
    pass


def postino_raw(text=None, html=None,
        subject=None,
        to=[], cc=[], bcc=[],
        cfg=None):

    if cfg is None:
        raise PostinoError('No configuration specified')

    if subject is None:
        raise PostinoError('No subject specified')

    if text is None and html is None:
        raise PostinoError('No body specified')

    if not compat.isunicode(subject):
        raise PostinoError('Subject must be a unicode string')

    if not (compat.isunicode(text) or compat.isunicode(html)):
        raise PostinoError('Body must be a unicode string')

    if not to:
        raise PostinoError('No recipients')

    for addr in to + cc + bcc:
        if not isinstance(addr, Address):
            raise PostinoError('Address of invalid type')

    def encode_text(text, encoding='utf-8'):
        if text is None:
            return None
        return (text.encode(encoding), encoding)

    convert_address = lambda addr: addr.to_pyzmail()
    convert_addresses = lambda a: [convert_address(e) for e in a]

    # all looks OK, create and send the email
    payload, mail_from, rcpt_to, msg_id = compose_mail(
            convert_address(cfg.sender),
            convert_addresses(to),
            cc=convert_addresses(cc),
            bcc=convert_addresses(bcc),
            subject=subject.replace('\n', ' ').strip(),
            default_charset='utf-8',
            text=encode_text(text),
            html=encode_text(html))

    ret = send_mail(payload,
                    mail_from, rcpt_to,
                    cfg.server,
                    smtp_port=cfg.port,
                    smtp_mode=cfg.mode,
                    smtp_login=cfg.login,
                    smtp_password=cfg.password)

    if ret:
        raise PostinoError('Failed sending: %s' % ret)


def process_addresses(addr):
    def addressify(obj):
        if isinstance(obj, Address):
            return obj
        else:
            return Address(addr)

    if not addr:
        return []

    if hasattr(addr, '__iter__') and not compat.isbasestring(addr):
        # iterable, but not a string
        addr_list = addr
    else:
        addr_list = [addr]

    return [addressify(a) for a in addr_list]


def postino(text=None, html=None,
        subject=None,
        to=None, cc=None, bcc=None,
        cfg=None):

    if not cfg:
        cfg = config.Config.load_default()

    if not cfg:
        raise PostinoError('No valid configuration found')

    return postino_raw(
            text=text,
            html=html,
            subject=subject if subject is not None else cfg.subject,
            to=process_addresses(to or cfg.to),
            cc=process_addresses(cc or cfg.cc),
            bcc=process_addresses(bcc or cfg.bcc),
            cfg=cfg)


def postino_markdown(text, subject=None,
        to=None, cc=None, bcc=None,
        cfg=None):

    html = markdown(text)
    return postino(text=text, html=html,
        subject=subject,
        to=to, cc=cc,
        cfg=cfg)



