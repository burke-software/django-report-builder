FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD setup.py /code/
RUN pip install -e . -r requirements.txt django==1.8
ADD . /code/
