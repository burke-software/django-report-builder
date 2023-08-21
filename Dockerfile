FROM python:3.8-slim
ENV PYTHONUNBUFFERED=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  PIP_DISABLE_PIP_VERSION_CHECK=on

RUN mkdir /code
WORKDIR /code
RUN pip install poetry
COPY poetry.lock pyproject.toml /code/
RUN poetry install --no-interaction --no-ansi --no-root
ADD . /code/
