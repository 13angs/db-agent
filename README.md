# Db Agent

[![Docker Build](https://github.com/13angs/db_agent/actions/workflows/docker-build-main.yml/badge.svg)](https://github.com/13angs/db_agent/actions/workflows/docker-build-main.yml)

## Setup the workspace

Clone the repository

```bash
git clone https://github.com/13angs/db_agent.git
```

Setup the .env file

```bash
cp samples/.env.sample .env
```

## Running Backup job

Change JOB_NAME in .env file to BACKUP

```bash
JOB_NAME=BACKUP
```

Change the root and docker id by running

```bash
id -nG
# or
id -G
```

Then set the id in .env file

```bash
ROOT_ID=0
DOCKER_ID=1001
```

Run the backup

```bash
docker-compose up -d
# OR
docker-compose up
```

## Running restore job

Repeat the backup job' steps
Change the .env file

```bash
JOB_NAME=RESTORE
```

Run the restore

```bash
docker-compose up -d
```
