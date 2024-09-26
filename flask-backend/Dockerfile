FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1


WORKDIR /flask-backend

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y wget

COPY . .

ENV FLASK_ENV=development
ENV PYTHONPATH=/flask-backend

EXPOSE 5000

CMD [ "python", "app.py" ]
