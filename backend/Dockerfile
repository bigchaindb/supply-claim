FROM python:3
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /
COPY ./requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

# copy the staging config to docker, which is what will be deployed on azure
# this should be in env settings at some point, this is just now & for dev
COPY ./conf/staging.cfg app.cfg

# copy the source code over, including the conf & startup stubs
COPY ./epcis_api/ ./epcis_api/
COPY ./runserver.py .
COPY ./conf.py .

CMD ["python", "runserver.py"]