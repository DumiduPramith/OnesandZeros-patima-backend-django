FROM python:3.8-slim

WORKDIR /app

COPY . /app

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt
