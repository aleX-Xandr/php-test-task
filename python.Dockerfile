FROM python:3.11-slim

COPY /parser/requirements.txt /parser/requirements.txt

COPY ./parser /parser

WORKDIR /parser

RUN apt-get update && apt-get install -y xvfb && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install --with-deps

CMD ["sleep", "infinity"]
