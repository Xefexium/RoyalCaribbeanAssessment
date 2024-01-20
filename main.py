from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error
import requests
import logging
import sys
import os

class TimezoneDBAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.timezonedb.com/v2.1'

    def get_timezone_list(self):
        endpoint = '/list-time-zone'
        params = {
            'key': self.api_key,
            'format': 'json'
        }

        response = requests.get(self.base_url + endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            return data['zones']
        else:
            return None


    def create_connection(self):
        conn = None
        try:
            conn = sqlite3.connect('./time_zone_db.db')
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def create_tzdb_timezones_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TZDB_TIMEZONES (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                zoneName TEXT,
                countryCode TEXT,
                countryName TEXT,
                timestamp INTEGER
            )
        ''')
    
    def create_tzdb_details_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TZDB_ZONE_DETAILS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                countryCode TEXT,
                countryName TEXT,
                zoneName TEXT,
                abbreviation TEXT,
                gmtOffset INTEGER,
                dst TEXT,
                timestamp INTEGER
            )
        ''')

    def create_tzdb_error_log_table(self, cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TZDB_ERROR_LOG (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                errorCode TEXT,
                message TEXT,
                timestamp INTEGER
            )
        ''')

if __name__ == '__main__':
    load_dotenv()
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    api_key = os.getenv('TIMEZONE_DB_API_KEY')

    if not api_key:
        logging.error('TimezoneDB API key not found. Please set the TIMEZONE_DB_API_KEY environment variable.')
        sys.exit(1)
    else:
        logging.info('TimezoneDB API key found.')

    api = TimezoneDBAPI(api_key)
