# -*- coding: utf-8 -*-

import json
import base64
from getpass import getpass
from urllib import request, parse

class JSONFile:
    __input = ""

    def __init__(self, input_file):
        self.__input = input_file

    def get_data(self):
        data = {}
        
        try:
            with open(self.__input) as json_file:
                data = json.load(json_file)
        except:
            raise Exception("Invalid json file")
            
        return data

class WTF:
    __input = {}

    __request_data = {}
    __request = {}
    __response = {}
    __response_data = ""
    
    def __init__(self, input_data):
        self.__input = input_data

        self.__request_data = self.__clean_data(self.__input)
        self.__create_request(self.__request_data)
    
    def __clean_data(self, data):
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
        try:
            if not self.__response_data:
                self.__response_data = self.__response.read().decode("utf-8")
        except:
            pass
    
        return self.__response_data
    
    def get_response_raw(self):
        return self.__response
    
    def get_response_type(self):
        return self.__response.headers.get('content-type')

    def get_request(self):
        return self.__request

    def get_request_data(self):
        return self.__request_data
    
            
        