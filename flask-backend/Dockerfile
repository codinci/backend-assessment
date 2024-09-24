FROM python:3.10-slim-buster

WORKDIR /flask-backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y wget

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]