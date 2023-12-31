from python:3.11-slim

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        build-essential libeccodes-dev curl

COPY requirements.txt .
RUN pip install -U pip &&  \
    pip install -r requirements.txt

WORKDIR /app
ENV PYTHONPATH=/app
