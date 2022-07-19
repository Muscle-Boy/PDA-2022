FROM ubuntu:20.04

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

# ---------------------------------------------------------
RUN apt update     

RUN apt install mongodb -y && apt install python3-pip -y \
&& apt install curl -y && apt install iputils-ping -y \
&& apt install traceroute -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

# ---------------------------------------------------------

CMD service mongodb start

CMD python3 main.py
