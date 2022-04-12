FROM python:3-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/calc

RUN pip install twisted

COPY server.py .

CMD ./server.py
