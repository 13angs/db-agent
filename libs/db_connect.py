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
import os
import sys
import time


class DbConnect:
    """
    This is a class for mathematical operations on complex numbers.

    Attributes:
        real (int): The real part of complex number.
        imag (int): The imaginary part of complex number.
    """
    # setup dialect, username, password
    DIALECT = 'mysql'
    DB_USER = 'root'
    DB_USER_PASSWORD = ''
    DB_HOST = ''
    DB_NAME = ''
    DOCKER_CMD = ''
    con = None

    def __init__(self, **kwargs):
        """
        The constructor for ComplexNumber class.

        Parameters:
           real (int): The real part of complex number.
           imag (int): The imaginary part of complex number.   
        """
        # self.DB_HOST = kwargs['host']
        # self.DIALECT = kwargs['dialect']
        self.DB_USER = kwargs['user']
        self.DB_USER_PASSWORD = kwargs['password']
        self.DB_NAME = kwargs['database']
        self.DOCKER_CMD = kwargs['docker_cmd']

    def drop_all_table(self, path):
        """
        Summary line.

        Drop all the existing talbe in mysql database

        Parameters:
        path (string): the absolute path for temp.sql file

        Returns:
        int: Description of return value

        References:
        1. https://tableplus.com/blog/2018/08/mysql-how-to-drop-all-tables.html

        """

        # get the temp file path
        temp = 'temp.sql'
        temp_file = os.path.join(path, temp)

        # disable foreign key check
        dis_fk_cmd = f'echo "SET FOREIGN_KEY_CHECKS = 0;" > {temp_file}'
        os.system(dis_fk_cmd)
        time.sleep(1)

        # Then dump the db with no data and drop all tables:
        dump_with_no_data_cmd = f'{self.DOCKER_CMD} mysqldump --add-drop-table --no-data -u root -p{self.DB_USER_PASSWORD} {self.DB_NAME} | grep \'DROP TABLE\' >> {temp_file}'
        os.system(dump_with_no_data_cmd)
        time.sleep(1)

        # Turn the foreign key check back on:
        en_fk_cmd = f'echo "SET FOREIGN_KEY_CHECKS = 1;" >> {temp_file}'
        os.system(en_fk_cmd)
        time.sleep(1)

        # Now restore the db with the dump file:
        res_db_cmd = f'{self.DOCKER_CMD} mysql -u root -p{self.DB_USER_PASSWORD} {self.DB_NAME} < {temp_file}'
        os.system(res_db_cmd)
        time.sleep(1)
