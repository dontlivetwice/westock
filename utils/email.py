import re
from settings import prod

VALID_EMAIL = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,20}$)'  # domain
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE)


import sendgrid
from sendgrid import SendGridClientError, SendGridServerError

WS_WELCOME_TEMPLATE = """\
    <div>
        <p>Hi %s,</p>

        <p>Thank you! You have been added to the WeStock waitlist.</p>
        <p>Interested in priority access? Get early access by referring your friends.
        The more friends that join, the sooner you will get access.</p>
        <p>Sincerely,</p>
        <p>The WeStock Team</p>
    </div>
"""


class EmailException(Exception):
    pass


def send_email(receiver, sender, subject, text_content, html_content):
    if not sender:
        sender = 'notifications@westock.io'

    sg = sendgrid.SendGridClient(prod.WS_SENDGRID_API_KEY, raise_errors=True)

    message = sendgrid.Mail()

    if not VALID_EMAIL.match(receiver):
        raise EmailException('Receiver email not valid: %s' % receiver)

    if not VALID_EMAIL.match(sender):
        raise EmailException('Sender email not valid: %s' % sender)

    if not sender.endswith('westock.io'):
        raise EmailException("Email delivery not allowed for senders outside of the westock.io domain")

    message.add_to(receiver)

    message.set_subject(subject)

    if text_content:
        message.set_text(text_content)

    if html_content:
        message.set_html(html_content)

    message.set_from(sender)

    try:
        status, msg = sg.send(message)
    except SendGridClientError:
        raise EmailException('SendGridClientError')
    except SendGridServerError:
        raise EmailException('SendGridServerError')

    return status, msg
