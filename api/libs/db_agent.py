import os
import time
from datetime import datetime
import pipes
import shutil
from .db_connect import DbConnect


class DbAgent:
    """
    DB_HOST
    """
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

    # user, password, database, backup_path, container
    def __init__(self, host, **kwargs):
        self.DB_HOST = host
        self.DB_USER = kwargs['user']
        self.DB_USER_PASSWORD = kwargs['password']
        self.DB_NAME = kwargs['database']
        self.BACKUP_PATH = kwargs['backup_path']
        self.CONTAINER_NAME = kwargs['container']
        self.DATETIME = kwargs['datetime']
        self.DOCKER_CMD = f'docker exec -i {self.CONTAINER_NAME}'

    def backup(self):
        # Checking if backup folder already exists or not. If not exists will create it.
        try:
            os.stat(self.TODAYBACKUPPATH)
        except Exception as e:
            print(e)
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
            dumpcmd = self.DOCKER_CMD + " mysqldump" + " -u " + self.DB_USER + " -p" + \
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

    def restore(self):
        """
        """
        # gzipped db name
        gzipped_db = f"{self.DB_NAME}.sql.gz"
        unzip_db = f"{self.DB_NAME}.sql"
        # get the current working directory
        cwd = os.getcwd()

        # get the backup and restore dir
        backup_dir = os.path.join(cwd, 'backup')
        restore_dir = os.path.join(cwd, 'restore')

        # get all the file in backup dir
        # and remove the .gitignore file
        dirs = os.listdir(backup_dir)
        dirs.remove('.gitignore')

        restore_dirs = os.listdir(restore_dir)
        restore_dirs.remove('.gitignore')

        # convert string dt to datetime
        # store the date and dir_name in dictionary
        date_dirs = [{'created_date': datetime.strptime(str_date, '%Y%m%d-%H%M%S'),
                      'dir_name': str_date}
                     for str_date in dirs]

        # resort the item as desc
        sorted_date_dir = sorted(
            date_dirs,
            key=lambda x: x['created_date'],
            reverse=True
        )

        # get the latest backup dir
        # check if the dir exist
        # create it in restore dir
        latest_bk_dir = sorted_date_dir[0]

        if not latest_bk_dir['dir_name'] in restore_dirs:
            print('create the new restore dir')

            # get the newest restore dir
            new_restore_dir = os.path.join(
                restore_dir, latest_bk_dir['dir_name'])

            os.mkdir(new_restore_dir)

            # copy the latest backup to the restore dir
            new_res_path = os.path.join(restore_dir, latest_bk_dir['dir_name'])
            bk_file_path = os.path.join(
                backup_dir, latest_bk_dir['dir_name'], gzipped_db)
            res_file_path = os.path.join(
                new_res_path, gzipped_db)
            shutil.copyfile(bk_file_path, res_file_path)
            time.sleep(1)

            # unzip the file
            unzip_cmd = f"gzip -dk {res_file_path}"
            os.system(unzip_cmd)
            time.sleep(1)

            # restore the db
            # drop the database
            # restore it using mysql cmd
            db_con = DbConnect(
                database=self.DB_NAME,
                user=self.DB_USER,
                password=self.DB_USER_PASSWORD,
                docker_cmd=self.DOCKER_CMD
            )

            # drop all the existing tables
            db_con.drop_all_table(new_res_path)

            # restore the db
            res_db_sql_cmd_path = os.path.join(new_res_path, unzip_db)
            res_db_cmd = f'{self.DOCKER_CMD} mysql -u root -p{self.DB_USER_PASSWORD} {self.DB_NAME} < {res_db_sql_cmd_path}'
            os.system(res_db_cmd)
            time.sleep(1)
