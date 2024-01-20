from dotenv import load_dotenv
import sqlite3
from sqlite3 import Error
import requests
import logging
import sys
import os

class TimezoneDBAPI:

    DATABASE_PATH = './time_zone_db.db'
    BASE_URL = 'http://api.timezonedb.com/v2.1'
    API_KEY = None
    cursor = None

    """ Singleton class for TimezoneDB API"""
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(TimezoneDBAPI, cls).__new__(cls)
            cls._instance.cursor = sqlite3.connect(cls.DATABASE_PATH)
        return cls._instance

    def __init__(self, api_key):
        self.API_KEY = api_key

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

    def get_timezone_list(self):
        endpoint = '/list-time-zone'
        params = {
            'key': self.api_key,
            'format': 'json'
        }

        response = requests.get(self.BASE_URL + endpoint, params=params)

        if response.status_code == 200:
            data = response.json()
            return data['zones']
        else:
            return None

if __name__ == '__main__':
    load_dotenv() # Setup use of .env file
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # Set logging to appear in console

    api_key = os.getenv('TIMEZONE_DB_API_KEY')

    if not api_key:
        logging.error('TimezoneDB API key not found. Please set the TIMEZONE_DB_API_KEY environment variable.')
        logging.info('API Key available for free at https://timezonedb.com/register')
        sys.exit(1)
    else:
        logging.info('TimezoneDB API key found.')

    api = TimezoneDBAPI(api_key)
