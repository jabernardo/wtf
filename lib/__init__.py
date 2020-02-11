# -*- coding: utf-8 -*-

import json
import base64
from getpass import getpass
from urllib import request, parse

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
        except:
            raise Exception("Invalid json file")

        return data

class WTF:
    """WTF! Console POST"""

    __input = {}

    __request_data = {}
    __request = {}
    __response = {}
    __response_data = ""
    
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
        
        self.__response = request.urlopen(self.__request)

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
