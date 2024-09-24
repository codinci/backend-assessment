FROM python:3.10-slim-buster

WORKDIR /flask-backend

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y wget

COPY . .

ENV FLASK_ENV=development

EXPOSE 5000

CMD [ "python", "app.py" ]
