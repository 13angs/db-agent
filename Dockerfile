# docker from docker refs: https://tomgregory.com/running-docker-in-docker-on-windows/
FROM python:3.7-alpine3.15

WORKDIR /usr/src/app

RUN apk add docker

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

# run docker as non-root user
RUN adduser -D 13angs

# run as 13angs
USER 13angs

# use the --group-add argument to run a Docker image with additional groups for the user
# The root group has id 0
# docker run --group-add 0 --group-add 1001 -v //var/run/docker.sock:/var/run/docker.sock 13angs/db-agent:latest /bin/sh -c "docker ps"
CMD [ "python3", "./main.py" ]