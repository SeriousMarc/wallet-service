FROM python:3.8-slim
MAINTAINER GURU
WORKDIR /workdir
COPY . /workdir

RUN apt-get update && pip install --upgrade pip setuptools wheel poetry

RUN poetry config virtualenvs.create false --local && \
    poetry config virtualenvs.in-project false --local && \
    poetry install

#CMD python -m wallet_service.app
