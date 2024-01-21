from dotenv import load_dotenv
import logging
import sys
import os
from timezoneDB import TimezoneDB
from timezoneDBAPI import TimezoneDBAPI

def get_api_key():
    api_key = os.getenv('TIMEZONE_DB_API_KEY')

    if not api_key:
        logging.error('TimezoneDB API key not found. Please set the TIMEZONE_DB_API_KEY environment variable.')
        logging.error('API Key available for free at https://timezonedb.com/register')
        sys.exit(1)
    else:
        logging.info('TimezoneDB API key found.')

    return api_key

"""
Example usage
"""
if __name__ == '__main__':

    load_dotenv() # Setup use of .env file
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) # Set logging to appear in console

    api_key = get_api_key()

    api = TimezoneDBAPI(api_key)
    db = TimezoneDB()

    timezones = api.get_timezone_list()
    db.insert_tzdb_timezones_table(timezones)

    zone_detail = api.get_timezone_by_position(40.689247, -74.044502)
    db.insert_tzdb_details_table(zone_detail)

    zone_detail = api.get_timezone_by_zone('America/New_York')
    db.insert_tzdb_details_table(zone_detail)