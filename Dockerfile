FROM python:3.7

RUN mkdir -p /code/

ADD . /code

WORKDIR /code/

ADD ./requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5000