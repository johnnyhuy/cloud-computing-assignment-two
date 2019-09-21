# FROM jfloff/alpine-python:3.7-slim
FROM tiangolo/uwsgi-nginx-flask:python3.7-alpine3.8

COPY app /app

RUN apk add --update alpine-sdk python3-dev
RUN pip install --requirement requirements.txt
