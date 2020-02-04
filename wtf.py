# -*- coding: utf-8 -*-

import json
from urllib import request, parse

class WTF:
    __input = ""
    
    __request_methods = ["GET", "POST", "PUT", "DELETE", "UPDATE", "HEAD", "OPTIONS"]    

    __request_data = {}
    __request = {}
    __response = {}
    
    def __init__(self, file):
        self.__input = file
        self.__shit()
    
    def __get_data(self):
        data = {}
        
        try:
            with open(self.__input) as json_file:
                data = json.load(json_file)
        except:
            raise Exception("Invalid json file")
            
        return data
    
    def __clean_data(self, data):
        if not "url" in data:
            raise Exception("No URL.")
        
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
        self.__request = request.Request(
                     url=data["url"],
                     method=data["method"],
                     headers=data["headers"],
                     data=bytes(parse.urlencode(data["data"]), encoding="utf-8")
                )
        
        self.__response = request.urlopen(self.__request)
    
    def __shit(self, formatted=True):
        data = self.__get_data()
        self.__request_data = self.__clean_data(data)
        self.__create_request(self.__request_data)

    def get_response(self):
        html = self.__response.read().decode("utf-8")
    
        return html
    
    def get_response_raw(self):
        return self.__response
    
    def get_response_type(self):
        return self.__response.headers.get('content-type')

    def get_request(self):
        return self.__request

    def get_request_data(self):
        return self.__request_data
    
            
        