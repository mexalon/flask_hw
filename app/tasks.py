import time

from celery import Celery

app = Celery(
    'tasks',
    broker='redis://127.0.0.1:6379/1',
    backend='redis://127.0.0.1:6379/2')


@app.task
def send_email(to, title, text):

    return f"{to}>>{title}>>{text}"


"""https://stackoverflow.com/questions/37255548/how-to-run-celery-on-windows"""