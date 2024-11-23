FROM python:3.12-slim
COPY ./client12.py ./
RUN apt-get update && apt-get install -y iproute2 && apt-get clean
