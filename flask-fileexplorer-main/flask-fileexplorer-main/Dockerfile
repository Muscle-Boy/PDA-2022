FROM python:3.9.13-slim-buster

WORKDIR /

COPY . ./

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD python3 setup.py

EXPOSE 80