#!/usr/bin/env python

import argparse
import sys

from markdown import markdown
from pyzmail import compose_mail, send_mail

import config


class PostinoError(Exception):
    pass


def postino(text=None, html=None,
        subject=None,
        to=None, cc=None,
        cfg=None):

    if not subject:
        raise PostinoError('No subject')

    if not text and not html:
        raise PostinoError('No body specified')

    if not cfg:
        cfg = config.Config.load_default()

    if not cfg:
        raise PostinoError('No valid configuration found')

    to = to or cfg.to
    if not to:
        raise PostinoError('No recipient specified')

    # all looks OK, create and send the email
    payload, mail_from, rcpt_to, msg_id = compose_mail(
            (cfg.name, cfg.user),
            to,
            subject,
            'utf-8',
            (text.encode('utf-8'), 'utf-8'),
            html=(html.encode('utf-8'), 'utf-8'))

    ret = send_mail(payload,
                    mail_from, rcpt_to,
                    cfg.server,
                    smtp_port=cfg.port,
                    smtp_mode=cfg.mode,
                    smtp_login=cfg.user,
                    smtp_password=cfg.password)

    if ret:
        raise PostinoError('Failed sending: %s' % ret)


def postino_markdown(text, subject=None,
        to=None, cc=None,
        cfg=None):

    html = markdown(text)
    return postino(text=text, html=html,
        subject=subject,
        to=to, cc=cc,
        cfg=cfg)


def main():
    parser = argparse.ArgumentParser('Send emails.')
    parser.add_argument('to', type=str, nargs='*')
    parser.add_argument('--markdown', '-m', action='store_true')
    parser.add_argument('--subject', '-s')

    args = parser.parse_args()

    text = [s.decode('utf-8') for s in sys.stdin.readlines()]

    if args.subject:
        # subject on command line
        subject = args.subject
        body = '\n'.join(text)
    else:
        # subject in first line
        subject = text[0]
        body = '\n'.join(text[1:])

    body = body.strip()

    try:
        if args.markdown:
            postino_markdown(subject=subject,
                    text=body,
                    to=args.to)
        else:
            postino(subject=subject,
                    text=body,
                    to=args.to)
    except PostinoError as e:
        raise SystemExit(e)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit('Aborted.')
