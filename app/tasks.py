
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery

import smtplib
import ssl

import config


app = Celery(
    'tasks',
    broker=f'{config.REDIS_URL}/0',
    backend=f'{config.REDIS_URL}/1',
)


def gmail_it(to, subject, text):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = config.DEV_EMAIL
    receiver_email = to
    password = config.DEV_PASS

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to

    message.attach(MIMEText(text, "plain"))
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


@app.task
def send_email(subject, text, to_list: list):
    [gmail_it(to, subject, text) for to in to_list]
    return f"{to_list}>>{subject}>>{text}"


""" Без этого не хочет работать из под винды """
""" celery -A tasks.app  worker -l info -P eventlet """
