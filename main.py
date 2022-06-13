# Import required python libraries

from libs.db_agent import Db_agent
import time

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.

DB_HOST = '172.28.80.226'
DB_USER = 'root'
DB_USER_PASSWORD = 'P@ssw0rd'
#DB_NAME = '/backup/dbnameslist.txt'
DB_NAME = 'WhappyvDb'
BACKUP_PATH = 'backup'
CONTAINER_NAME = 'db_agent-db-1'
DOCKER_CMD = f'docker exec {CONTAINER_NAME}'

# Getting current DateTime to create the separate backup folder like "20180817-123433".
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

agent = Db_agent()

agent.backup()
