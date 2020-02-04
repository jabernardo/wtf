#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:07:34 2020

@author: jabernardo
"""

import argparse
import json

from wtf import WTF
from pygments import highlight, lexers, formatters

def colorized(response, response_type):
    response_formatted = response
    
    if "application/json" in response_type:
        jsonified = json.loads(response)
        formatted_json = json.dumps(jsonified, sort_keys=True, indent=4)
        response_formatted = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    
    if "text/html" in response_type:
        response_formatted = highlight(response, lexers.HtmlLexer(), formatters.TerminalFormatter())
    
    return response_formatted

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="wtf.json", help="File input")
    parser.add_argument("-r", "--raw", action="store_true", default=False, help="Colored output")
    args = parser.parse_args()
    
    shit = WTF(args.file)
    response = shit.get_response()
    
    if not args.raw:
        response = colorized(response, shit.get_response_type())
    
    request_data = shit.get_request_data()
    response_data = shit.get_response_raw()
    
    print(f'LABEL: {request_data["label"]}')
    print(f'URL: {request_data["url"]}')
    print(f'METHOD: {request_data["method"]}')
    print(f'STATUS: {response_data.status} {response_data.reason}')
    print(f'DATA:\n{response}')

if __name__ == "__main__":
    main()
