import requests
import logging
from timezoneDB import TimezoneDB

class TimezoneDBAPI:

    BASE_URL = 'http://api.timezonedb.com/v2.1'
    API_KEY: str = None

    def __init__(self, api_key):
        self.API_KEY = api_key

    def __request(self, endpoint, params):
        response = requests.get(self.BASE_URL + endpoint, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_timezone_list(self):
        response = self.__request('/list-time-zone', {
            'key': self.API_KEY,
            'format': 'json'
        })

        if response:
            return response['zones']
        else:
            return None

    def get_timezone_by_zone(self, zone):
        response = self.__request('/get-time-zone', {
            'key': self.API_KEY,
            'format': 'json',
            'by': 'zone',
            'zone': zone
        })

        if response:
            return response
        else:
            return None

    def get_timezone_by_position(self, lat, lng):
        response = self.__request('/get-time-zone', {
            'key': self.API_KEY,
            'format': 'json',
            'by': 'position',
            'lat': lat,
            'lng': lng
        })

        if response:
            return response
        else:
            return None


