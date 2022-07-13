FROM python:latest

WORKDIR $APP_HOME

ENV /APP_HOME/ app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . ./

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
