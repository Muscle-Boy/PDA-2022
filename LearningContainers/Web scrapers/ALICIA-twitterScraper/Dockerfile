FROM python:3
WORKDIR /app
ADD . /app
RUN chown -R "$USER" /app
USER "$USER"
RUN chmod -R 777 /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 7000
CMD [ "python3", "app.py" ]