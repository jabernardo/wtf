#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:07:34 2020

@author: jabernardo
"""

import argparse
import json

from wtf import WTF, JSONFile
from getpass import getpass
from pygments import highlight, lexers, formatters
from colored import fore, back, style

def colorized(response, response_type):
    response_formatted = response
    
    if "application/json" in response_type:
        jsonified = json.loads(response)
        formatted_json = json.dumps(jsonified, sort_keys=True, indent=4)
        response_formatted = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    
    if "text/html" in response_type:
        response_formatted = highlight(response, lexers.HtmlLexer(), formatters.TerminalFormatter())
    
    return response_formatted

def authenticate():
    auth = {}

    auth["username"] = input("Username: ")
    auth["password"] = getpass("Password: ")

    return auth

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="wtf.json", help="File input")
    parser.add_argument("-r", "--raw", action="store_true", default=False, help="Colored output")
    args = parser.parse_args()
    
    try:
        data = JSONFile(args.file).get_data()

        if "authentication" in data:
            data["authentication"] = authenticate()

        shit = WTF(data)
        response = shit.get_response()

        if not args.raw:
            response = colorized(response, shit.get_response_type())
        
        request_data = shit.get_request_data()
        response_data = shit.get_response_raw()
        
        status_color = fore.GREEN

        if response_data.status != 200:
            status_color = fore.RED

        print(f'{fore.LIGHT_GREEN}{style.BOLD}{request_data["label"]}{style.RESET}')
        print(f'{style.BOLD}URL: {fore.BLUE}{request_data["url"]}{style.RESET}')
        print(f'{style.BOLD}METHOD: {fore.BLUE}{request_data["method"]}{style.RESET}')
        print(f'{style.BOLD}STATUS: {status_color}{response_data.status} {response_data.reason}{style.RESET}')
        print(f'{style.BOLD}DATA:\n{response}{style.RESET}')
    except Exception as err:
        print(f'{back.RED}{style.BOLD}{err}{style.RESET}\n')

if __name__ == "__main__":
    main()
