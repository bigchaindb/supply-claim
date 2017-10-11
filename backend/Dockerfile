FROM python:3
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /
COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY ./conf/flask-docker-compose.cfg app.cfg
COPY ./epcis_api/ ./epcis_api/
COPY ./runserver.py .
COPY ./conf.py .

CMD ["python", "runserver.py"]