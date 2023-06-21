from . import mail
from flask_mail import Message
from app import templates


def send_email(recipient, stylesheet):
    msg = Message('Chat login verification code.',
                  sender='kacperdusza22@gmail.com',
                  recipients=[recipient],
                  html=stylesheet)
    mail.send(msg)
