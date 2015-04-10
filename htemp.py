# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#
# apt-get install python-daemon python-lockfile

import os
import logging
import time
import sqlite3
from daemon import runner

# Logger setup
logger = logging.getLogger("htemp")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/htemp.log")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Db():

    DB_PATH = os.path.abspath(os.path.dirname(__file__))
    TABLE_NAME = 'HTEMP'
    TABLE_SCHEMA = '''CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY,
                                    temp REAL,
                                    humidity REAL,
                                    time INT
                                    );
                   ''' % TABLE_NAME
    db = None
    cursor = None

    def __init__(self):
        try:
            open(os.path.join(self.DB_PATH, 'sqlite_htemp.db'), 'a')
            self.sqlite_connect()
            self.sqlite_checkTable()
        except Exception as e:
            logger.error("Exception with sqlite initialization: %s" % e)

    def sqlite_connect(self):
        self.db = sqlite3.connect(os.path.join(self.DB_PATH, 'sqlite_htemp.db'))
        self.cursor = self.db.cursor()

    def sqlite_checkTable(self):
        try:
            logger.info("Checking existance of %s table" % self.TABLE_NAME)
            self.cursor.execute('''PRAGMA journal_mode = OFF''')
            self.cursor.execute(self.TABLE_SCHEMA)
            self.db.commit()
        except Exception as e:
            logger.error("Exception with SQL table: %s" % e)

    def sqlite_execute(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            logger.error("Exception with SQL query: %s" % e)


class App():
    #Instance DB
    db = Db()

    def __init__(self):
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.run_dir = os.path.join(self.root, "run")
        self.stdin_path = '/dev/null'
        self.stdout_path = os.path.join(self.run_dir, 'stdout.txt')
        self.stderr_path = os.path.join(self.run_dir, 'stderr.txt')
        self.pidfile_path = os.path.join(self.run_dir, 'test.pid')
        self.pidfile_timeout = 5

    def run(self):
        i = 0
        while True:
            epoch_time = int(time.time())
            i += 1
            self.db.cursor.execute('''INSERT INTO %s(temp, humidity, time)
                VALUES(?,?,?)''' % self.db.TABLE_NAME, (i, i, epoch_time))
            self.db.commit()
            logger.debug("Debug message %s" % i)
            time.sleep(5)

#Class instance
app = App()
daemon_runner = runner.DaemonRunner(app)
#Avoid logger file close during execution
daemon_runner.daemon_context.files_preserve = [handler.stream]
#Execute run method from app instance
daemon_runner.do_action()
