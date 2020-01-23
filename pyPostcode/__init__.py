#!/usr/bin/python
# -*- coding: utf-8 -*-


'''
pyPostcode by Stefan Jansen
pyPostcode is an api wrapper for http://postcodeapi.nu
'''

from urllib.request import urlopen, Request

import json
import logging


__version__ = '0.5'


class pyPostcodeException(Exception):

    def __init__(self, id, message):
        self.id = id
        self.message = message


class Api(object):

    def __init__(self, api_key, api_version=(3, 0, 0)):
        if api_key is None or api_key is '':
            raise pyPostcodeException(
                0, "Please request an api key on http://postcodeapi.nu")

        self.api_key = api_key
        self.api_version = api_version
        self.url = 'https://api.postcodeapi.nu'

    def handleresponseerror(self, status):
        if status == 401:
            msg = "Access denied! Api-key missing or invalid"
        elif status == 404:
            msg = "No result found"
        elif status == 500:
            msg = "Unknown API error"
        else:
            msg = "dafuq?"

        raise pyPostcodeException(status, msg)

    def request(self, path=None):
        '''Helper function for HTTP GET requests to the API'''

        headers = {
            "Accept": "application/json",
            "Accept-Language": "en",
            "X-Api-Key": self.api_key,
        }

        result = urlopen(Request(
            self.url + path, headers=headers,
        ))

        if result.getcode() is not 200:
            self.handleresponseerror(result.getcode())

        resultdata = result.read()

        if isinstance(resultdata, bytes):
            resultdata = resultdata.decode("utf-8")  # for Python 3
        jsondata = json.loads(resultdata)

        if jsondata:
            data = jsondata
        else:
            data = None

        return data

    def getaddress(self, postcode, house_number):
        path = '/v3/lookup/{0}/{1}'
        path = path.format(
            str(postcode),
            str(house_number))

        try:
            data = self.request(path)
        except pyPostcodeException as e:
            logging.error(
                'Error looking up %s%s%s on %s: %d %s',
                postcode, house_number and ' ' or '', house_number, self.url,
                e.id, e.message)
            data = None
        except Exception as e:
            logging.exception(e)
            data = None

        if data is not None:
            return Resource(data)
        else:
            return False


class Resource(object):

    def __init__(self, data):
        self._data = data

    @property
    def street(self):
        return self._data['street']

    @property
    def house_number(self):
        return self._data.get('number', self._data.get('house_number'))

    @property
    def postcode(self):
        return self._data.get('postcode')

    @property
    def town(self):
        return self._data.get('city')

    @property
    def municipality(self):
        result = self._data.get('municipality', {})
        if isinstance(result, dict):
            result = result.get('label')
        return result

    @property
    def province(self):
        result = self._data.get('province', {})
        if isinstance(result, dict):
            result = result.get('label')
        return result
