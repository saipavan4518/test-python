#syntax=docker/dockerfile:1

FROM python:slim-buster

WORKDIR /backend

COPY requirements.txt requirements.txt

CMD ["python3","-m","venv","venv"]

CMD ["source","venv\bin\activate"]

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3","server.py"]
