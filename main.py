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
    API_KEY: str = None
    _instance = None
    cursor: sqlite3.Connection = None

    """ Singleton class for TimezoneDB API"""
    def __new__(cls, api_key):
        if not cls._instance:
            cls._instance = super(TimezoneDBAPI, cls).__new__(cls)
            cls._instance.cursor = sqlite3.connect(cls.DATABASE_PATH)
            cls.API_KEY = api_key
        return cls._instance

    def __init__(self, api_key): # API key initalized in the __new__ method
        self.create_tzdb_timezones_table()
        self.create_tzdb_details_table()
        self.create_tzdb_error_log_table()

    def create_tzdb_timezones_table(self):
        logging.info('Dropping TZDB_TIMEZONES table if exists')
        self.cursor.execute('DROP TABLE IF EXISTS TZDB_TIMEZONES')
        logging.info('Creating TZDB_TIMEZONES table')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TZDB_TIMEZONES (
                countryCode TEXT CHECK(LENGTH(countryCode) <= 2),
                countryName TEXT CHECK(LENGTH(countryName) <= 100),
                zoneName TEXT PRIMARY KEY CHECK(LENGTH(zoneName) <= 100),
                gmtOffset INTEGER,
                import_date INTEGER
            )
        ''')
    
    def create_tzdb_details_table(self):
        logging.info('Creating TZDB_ZONE_DETAILS table')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TZDB_ZONE_DETAILS (
                countryCode TEXT,
                countryName TEXT,
                zoneName TEXT PRIMARY KEY,
                gmtOffset INTEGER,
                dst INTEGER,
                zoneStart INTEGER,
                zoneEnd INTEGER,
                import_date INTEGER
            )
        ''')

    def create_tzdb_error_log_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TZDB_ERROR_LOG (
                error_date INTEGER,
                error_message TEXT CHECK(LENGTH(error_message) <= 1000)
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
