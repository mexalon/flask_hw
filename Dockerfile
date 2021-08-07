FROM python:3.8
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
WORKDIR /app
RUN celery -A tasks.app  worker -c 2
ENTRYPOINT ["python", "main.py"]

