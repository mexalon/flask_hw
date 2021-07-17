FROM python:3.8
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
WORKDIR /app
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]

