# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#
# apt-get install python-daemon python-lockfile

import os
import time
from db import Db
from daemon import runner
from logger import handler, logger


class App():

    def __init__(self):
        self.root = os.path.abspath(os.path.dirname(__file__))
        self.run_dir = os.path.join(self.root, "run")
        self.stdin_path = '/dev/null'
        self.stdout_path = os.path.join(self.run_dir, 'stdout.log')
        self.stderr_path = os.path.join(self.run_dir, 'stderr.log')
        self.pidfile_path = os.path.join(self.run_dir, 'htemp.pid')
        self.pidfile_timeout = 5

    def run(self):
        # http://stackoverflow.com/questions/26831624/python-daemon-can-see-database-but-complains-that-tables-do-not-exist
        # Python daemon closes all open file descriptors (except stdin, stout and stderr) when you daemonise.
        # I spent ages trying to figure out which files to keep open to prevent my database from being inaccessible, and in the end I found that it's easier to initialise the database inside the daemon context rather than outside. That way I don't need to worry about which files should stay open.
        # Now everything is working fine.
        #Instance DB
        db = Db()
        i = 0
        while True:
            epoch_time = int(time.time())
            i += 1
            db.cursor.execute('INSERT INTO %s(temp, humidity, time) VALUES(?,?,?);' % db.TABLE_NAME, (1, 1, epoch_time))
            db.conn.commit()
            logger.debug("Debug message %s" % i)
            time.sleep(5)

#Class instance
app = App()
#app.run()
daemon_runner = runner.DaemonRunner(app)
#Avoid logger file close during execution
daemon_runner.daemon_context.files_preserve = [handler.stream]
#Execute run method from app instance
daemon_runner.do_action()
