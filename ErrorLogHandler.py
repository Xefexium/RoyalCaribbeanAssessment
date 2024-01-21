import logging
import time
from sqlite3 import Connection, Error

class ErrorLogHandler(logging.Handler):

    def __init__(self, sql_cursor):
        logging.Handler.__init__(self)
        self.cursor: Connection = sql_cursor

    def emit(self, record):

        if not record.levelname == 'ERROR':
            return

        error_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(record.created))

        error_message = f'File: {record.filename} Line: {record.lineno} {record.msg}' 
        try:
            logging.error('Logging error to DB: %s' % error_message)
            self.cursor.execute('''
                INSERT INTO TZDB_ERROR_LOG (error_date, error_message)
                VALUES (?, ?)
        ''', (error_date, error_message))
            self.cursor.commit()

        except Error as e:
            logging.error('Logging to DB failed with error: %s' % e)