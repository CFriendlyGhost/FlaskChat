from . import mail
from email_service import mail_config as m_c
from flask_mail import Message


def send_email(recipient, stylesheet):
    data = m_c.load_json()

    msg = Message('Chat login verification code.',
                  sender= data["email"],
                  recipients=[recipient],
                  html=stylesheet)
    mail.send(msg)
