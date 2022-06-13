# docker from docker refs: https://tomgregory.com/running-docker-in-docker-on-windows/
FROM python:3.7-alpine3.15

WORKDIR /usr/src/app

RUN apk add docker

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD [ "python3", "./main.py" ]