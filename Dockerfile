FROM python:3.10-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src /usr/src/app/

EXPOSE 8080

CMD ["python3", "main.py"]