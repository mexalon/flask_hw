import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery

import smtplib
import ssl
from config import DEV_EMAIL, DEV_PASS

app = Celery(
    'tasks',
    broker='redis://127.0.0.1:6379/1',
    backend='redis://127.0.0.1:6379/2')


def gmail_it(to, title, text):
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = DEV_EMAIL
    receiver_email = 'nabarysh@gmail.com'
    password = DEV_PASS

    message = MIMEMultipart()
    message["Subject"] = title
    message["From"] = sender_email
    message["To"] = to

    message.attach(MIMEText(text, "plain"))
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


@app.task
def send_email(to, title, text):
    time.sleep(10)
    gmail_it(to, title, text)
    time.sleep(10)
    return f"{to}>>{title}>>{text}"


""" Без этого не хочет работать из под винды """
""" celery -A tasks.app  worker -l info -P eventlet """
