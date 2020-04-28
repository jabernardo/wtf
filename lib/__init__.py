# -*- coding: utf-8 -*-

import json
import base64
import re

from getpass import getpass
from urllib import request, parse
from time import time

class JSONFile:
    """JSON File parser"""

    # File path
    __input = ""

    def __init__(self, input_file):
        """JSON File parser\n

        \nArguments:\n
        :param input_file (str) -- Source file path
        
        """
        self.__input = input_file

    def get_data(self):
        """Read json data\n

        \nReturn:\n
        `dict` -- Parsed JSON file
        """

        data = {}
        
        try:
            with open(self.__input) as json_file:
                data = json.load(json_file)
                json_file.close()
        except:
            raise Exception("Invalid json file")

        return data

class ArgumentsParser:
    __data = {}

    def __init__(self, args):
        """Create request data based from arguments\n
        \nArguments:\n:
        `args` (dict) -- Command-line arguments\n
        """

        self.__data = {
            "url": args.source,
            "method": args.method
        }

        if args.data:
            self.__data["data"] = self.__parse_data(args.data)

        if args.header:
            self.__data["headers"] = self.__parse_data(args.header)

        if args.login:
            self.__data["authentication"] = True

    def __parse_data(self, data):
        if isinstance(data, list):
            return_data = {}

            for value in data:
                matches = re.findall(r"(\w+)=(.*)", value[0])

                if matches:
                    key, val = matches[0]
                    return_data[key] = val

            return return_data

        return return_data

    def items(self):
        """Get data
        \nReturns:\n:
        `dict`
        """
        return self.__data

class WTF:
    """WTF! Console POST"""

    __input = {}

    __request_data = {}
    __request = {}
    __response = {}
    __response_data = ""

    __profile = {}
    
    def __init__(self, input_data):
        """WTF! Console POST\n

        \nArguments:\n
        `input_data` (dict) Request information
        """

        if not type(input_data) == dict:
            raise Exception("Input must be a dictionary")

        self.__input = input_data

        self.__request_data = self.__clean_data(self.__input)
        self.__create_request(self.__request_data)
    
    def __clean_data(self, data):
        """Sanitize input data\n

        \nArguments:\n
        `data` (dict) -- Input data

        \nReturns:\n
        `dict`
        """

        if not "url" in data:
            raise Exception("No URL.")
        
        if "authentication" in data:
            if not "username" in data["authentication"] and not "password" in data["authentication"]:
                raise Exception("Authentication Required")

        if not "label" in data:
            data["label"] = data["url"]

        if not "method" in data:
            data["method"] = "GET"
        
        if not "headers" in data:
            data["headers"] = {}
        else:
            if not type(data["headers"]) is dict:
                raise Exception("Invalid headers")
                
        if not "data" in data:
            data["data"] = {}
            
        else:
            if not type(data["data"]) is dict:
                raise Exception("Invalid data")
            
        return data


    def __create_request(self, data):
        """Create request object

        \nArguments:\n
        `data` (dict) -- Input data

        \nReturns:\n
        None
        """

        if "authentication" in data:
            creds = data["authentication"]
            auth = base64.b64encode("{0}:{1}".format(creds["username"], creds["password"]).encode())
            data["headers"]["Authorization"] = "Basic {0}".format(auth.decode())

        self.__request = request.Request(
                     url=data["url"],
                     method=data["method"],
                     headers=data["headers"],
                     data=bytes(parse.urlencode(data["data"]), encoding="utf-8"),
                     unverifiable=True
                )
        
        time_start = time()
        self.__response = request.urlopen(self.__request)
        time_stop = time()

        self.__profile["time"] = time_stop - time_start

    def get_response(self):
        """Get response

        \nReturns:\n
        `str`
        """
        try:
            if not self.__response_data:
                self.__response_data = self.__response.read().decode("utf-8")
        except:
            pass
    
        return self.__response_data
    
    def get_response_raw(self):
        """Get response object

        \nReturns:\n
        `Response`
        """

        return self.__response
    
    def get_response_type(self):
        """Get response type

        \nReturns:\n
        `str`
        """
        return self.__response.headers.get('content-type')

    def get_request(self):
        """Get request object

        \nReturns:\n
        `class`
        """
        return self.__request

    def get_request_data(self):
        """Get request data

        \nReturns:\n
        `dict`
        """
        return self.__request_data

    def get_profile(self, key = None):
        if not key is None:
            return None if not key in self.__profile else self.__profile[key]

        return self.__profile
