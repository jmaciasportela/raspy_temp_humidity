# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

import os
import sqlite3
import logging


class Db():

    DB_PATH = os.path.abspath(os.path.dirname(__file__))
    TABLE_NAME = 'HTEMP'
    TABLE_SCHEMA = '''CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY,
                                    temp REAL,
                                    humidity REAL,
                                    time INT
                                    );
                   ''' % TABLE_NAME
    conn = None
    cursor = None
    logger = logging.getLogger("htemp")

    def __init__(self):
        try:
            open(os.path.join(self.DB_PATH, 'sqlite_htemp.db'), 'a')
            self.sqlite_connect()
            self.sqlite_checkTable()
        except Exception as e:
            self.logger.error("Exception with sqlite initialization: %s" % e)

    def sqlite_connect(self):
        self.conn = sqlite3.connect(os.path.join(self.DB_PATH, 'sqlite_htemp.db'))
        self.cursor = self.conn.cursor()

    def sqlite_checkTable(self):
        try:
            self.logger.info("Checking existance of %s table" % self.TABLE_NAME)
            self.cursor.execute(self.TABLE_SCHEMA)
            self.conn.commit()
        except Exception as e:
            self.logger.error("Exception with SQL table: %s" % e)

    def sqlite_execute(self, sql):
        try:
            self.cursor.execute(sql)
        except Exception as e:
            self.logger.error("Exception with SQL query: %s" % e)
