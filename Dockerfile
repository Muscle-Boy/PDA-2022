FROM ubuntu:20.04

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./


RUN apt update     

RUN apt install mongodb -y && apt install python3-pip -y \
apt install curl -y

RUN service mongodb start


RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD python3 main.py
