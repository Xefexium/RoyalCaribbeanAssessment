import sqlite3
import logging

class TimezoneDB:

    DATABASE_PATH = './timezonedb.db'
    _instance = None
    cursor: sqlite3.Connection = None

    """Singleton class for TimezoneDB"""
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(TimezoneDB, cls).__new__(cls)
            cls._instance.cursor = sqlite3.connect(cls.DATABASE_PATH)
        return cls._instance

    def __init__(self):
        self.__create_tzdb_timezones_table()
        self.__create_tzdb_details_table()
        self.__create_tzdb_error_log_table()

    def __create_tzdb_timezones_table(self):
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
    
    def __create_tzdb_details_table(self):
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

    def __create_tzdb_error_log_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TZDB_ERROR_LOG (
                error_date INTEGER,
                error_message TEXT CHECK(LENGTH(error_message) <= 1000)
            )
        ''')

    def insert_tzdb_timezones_table(self, timezones):
        for timezone in timezones:
            logging.info('Inserting timezone: %s to TZDB_TIMEZONES', timezone['zoneName'])
            self.cursor.execute('''
                INSERT INTO TZDB_TIMEZONES (
                    countryCode,
                    countryName,
                    zoneName,
                    gmtOffset,
                    import_date
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                timezone['countryCode'],
                timezone['countryName'],
                timezone['zoneName'],
                timezone['gmtOffset'],
                timezone['timestamp']
            ))
        self.cursor.commit()

    def insert_tzdb_details_table(self, zone_detail):
        logging.info('Inserting timezone detail: %s to TZDB_ZONE_DETAILS', zone_detail['zoneName'])
        self.cursor.execute('''
            INSERT INTO TZDB_ZONE_DETAILS (
                countryCode,
                countryName,
                zoneName,
                gmtOffset,
                dst,
                zoneStart,
                zoneEnd,
                import_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            zone_detail['countryCode'],
            zone_detail['countryName'],
            zone_detail['zoneName'],
            zone_detail['gmtOffset'],
            zone_detail['dst'],
            zone_detail['zoneStart'],
            zone_detail['zoneEnd'],
            zone_detail['timestamp']
        ))
        self.cursor.commit()

