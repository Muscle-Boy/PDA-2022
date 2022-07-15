FROM ubuntu:20.04

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./


RUN sudo apt update     

RUN sudo apt install mongodb -y

RUN sudo systemctl start mongodb


RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD python3 main.py
