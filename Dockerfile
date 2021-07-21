FROM python:3.8
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./app /app
WORKDIR /app
ENV POSTGRE_URI = postgres://xytohjxhktxhou:d68b4315f9830dbe95b60775cd8b2100d8ed5bad7389c32e9e7ff7f3eeee68f3@ec2-34-242-89-204.eu-west-1.compute.amazonaws.com:5432/d2bcofjhgpfoh5
ENTRYPOINT ["python", "main.py"]

