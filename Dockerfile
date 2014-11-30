FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update -qq && apt-get install -y postgresql-client
RUN mkdir /code
WORKDIR /code
ADD setup.py /code/
RUN pip install -e .
ADD . /code/
