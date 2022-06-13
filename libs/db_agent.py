import os
import time
import datetime
import pipes


class Db_agent:
    DB_HOST = 'localhost'
    DB_USER = ''
    DB_USER_PASSWORD = 'root'
    #DB_NAME = '/backup/dbnameslist.txt'
    DB_NAME = ''
    BACKUP_PATH = 'backup'
    CONTAINER_NAME = ''
    DOCKER_CMD = f'docker exec {CONTAINER_NAME}'

    # Getting current DateTime to create the separate backup folder like "20180817-123433".
    DATETIME = time.strftime('%Y%m%d-%H%M%S')
    TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

    def __init__(self, host, user, password, database, backup_path, container):
        self.DB_HOST = host
        self.DB_USER = user
        self.DB_USER_PASSWORD = password
        self.DB_NAME = database
        self.BACKUP_PATH = backup_path
        self.CONTAINER_NAME = container
        self.DOCKER_CMD = f'docker exec {self.CONTAINER_NAME}'

    def backup(self):
        # Checking if backup folder already exists or not. If not exists will create it.
        try:
            os.stat(self.TODAYBACKUPPATH)
        except:
            os.mkdir(self.TODAYBACKUPPATH)

        # Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
        print("checking for databases names file.")
        if os.path.exists(self.DB_NAME):
            file1 = open(self.DB_NAME)
            multi = 1
            print("Databases file found...")
            print("Starting backup of all dbs listed in file " + self.DB_NAME)
        else:
            print("Databases file not found...")
            print("Starting backup of database " + self.DB_NAME)
            multi = 0

        # Starting actual database backup process.
        if multi:
            in_file = open(self.DB_NAME, "r")
            flength = len(in_file.readlines())
            in_file.close()
            p = 1
            dbfile = open(self.DB_NAME, "r")

            while p <= flength:
                db = dbfile.readline()   # reading database name from file
                db = db[:-1]         # deletes extra line
                dumpcmd = self.DOCKER_CMD + " mysqldump -h " + self.DB_HOST + " -u " + self.DB_USER + " -p" + \
                    self.DB_USER_PASSWORD + " " + db + " > " + \
                    pipes.quote(self.TODAYBACKUPPATH) + "/" + db + ".sql"
                os.system(dumpcmd)
                gzipcmd = "gzip " + \
                    pipes.quote(self.TODAYBACKUPPATH) + "/" + db + ".sql"
                os.system(gzipcmd)
                p = p + 1
            dbfile.close()
        else:
            print(f"dumping the database {self.DB_NAME}")
            db = self.DB_NAME
            dumpcmd = self.DOCKER_CMD + " mysqldump -h " + self.DB_HOST + " -u " + self.DB_USER + " -p" + \
                self.DB_USER_PASSWORD + " " + db + " > " + \
                pipes.quote(self.TODAYBACKUPPATH) + "/" + db + ".sql"
            os.system(dumpcmd)
            gzipcmd = "gzip " + \
                pipes.quote(self.TODAYBACKUPPATH) + "/" + db + ".sql"
            os.system(gzipcmd)

        print("")
        print("Backup script completed")
        print("Your backups have been created in '" +
              self.TODAYBACKUPPATH + "' directory")

    def show(self):
        print(self.TODAYBACKUPPATH)
