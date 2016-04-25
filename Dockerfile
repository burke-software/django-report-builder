FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
ADD requirements-dev.txt /code/
ADD setup.py /code/
RUN pip install -e . -r requirements.txt
RUN pip install -e . -r requirements-dev.txt
ADD . /code/
