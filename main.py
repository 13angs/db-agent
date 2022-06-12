#!/usr/bin/python

###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Rahul Kumar
# Website: http://tecadmin.net
# Created date: Dec 03, 2013
# Last modified: Aug 17, 2018
# Tested with : Python 2.7.15 & Python 3.5
# Script Revision: 1.4
#
##########################################################

# Install required libraries
# sudo apt install mysql-client

# Notes
# pip freeze > requirements.txt
# pip install -r requirements.txt

# Import required python libraries
import mysql.connector

# setup dialect, username, password
DIALECT = 'mysql'
USERNAME = 'root'
PASSWORD = ''
HOST = ''
DB_NAME = ''

mysqldb = mysql.connector.connect(
    host=HOST,
    user=USERNAME,
    password=PASSWORD,
    database=DB_NAME
)

cursor = mysqldb.cursor()

# gettin all the table names
cursor.execute("SHOW TABLES;")

table_names = []

# add all table name to a array
for record in cursor.fetchall():
    table_names.append(record[0])

backup_name = DB_NAME + '_BACKUP'

try:
    cursor.execute(f'CREATE DATABASE {backup_name}')
except:
    pass

for table_name in table_names:
    cursor.execute(
        f'CREATE TABLE {table_name} SELECT * FROM {DB_NAME}.{table_name}'
    )
