# Import required python libraries
from datetime import datetime
import os
from dotenv import load_dotenv
from libs.db_agent import DbAgent
import sys
import time

# load the env
# https://www.twilio.com/blog/environment-variables-python
load_dotenv()

# get require envs
JOB_NAME = os.environ['JOB_NAME']
DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_USER_PASSWORD = os.environ['DB_USER_PASSWORD']
DB_NAME = os.environ['DB_NAME']
BACKUP_PATH = os.environ['BACKUP_PATH']
CONTAINER_NAME = os.environ['CONTAINER_NAME']
DATETIME=time.strftime('%Y%m%d-%H%M%S')

# save the print message into file
sys.stdout = open(f'./data/logs/{DATETIME}.txt', 'w')

agent = DbAgent(
    DB_HOST,
    user=DB_USER,
    password=DB_USER_PASSWORD,
    database=DB_NAME,
    backup_path=BACKUP_PATH,
    container=CONTAINER_NAME,
    datetime=DATETIME
)

if JOB_NAME == 'BACKUP':
    agent.backup()
elif JOB_NAME == 'RESTORE':
    agent.restore()
