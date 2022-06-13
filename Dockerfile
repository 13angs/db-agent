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
# if the docker need to create a file/folder
# map that folder using docker volume if not it will throw an error
# v backup:/usr/src/app/backup 13angs/db-agent:latest
# Traceback (most recent call last):
# File "./main.py", line 26, in <module>
# os.stat(TODAYBACKUPPATH)
# FileNotFoundError: [Errno 2] No such file or directory: 'backup/20220613-055225'

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
# File "./main.py", line 28, in <module>
# os.mkdir(TODAYBACKUPPATH)
# PermissionError: [Errno 13] Permission denied: 'backup/20220613-055225'
# run the command exp:
# docker run --group-add 0 --group-add 1001 -v /var/run/docker.sock:/var/run/docker.sock -v /home/romdon/development/projects/13/db_agent/backup:/usr/src/app/backup 13angs/db-agent:latest
CMD [ "python3", "./main.py" ]