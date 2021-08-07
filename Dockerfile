FROM python:3.8
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./my_script.sh /app/
COPY ./app /app
WORKDIR /app
CMD ["sh", "my_script.sh"]


