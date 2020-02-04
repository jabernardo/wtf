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
    
    if "/json" in response_type:
        jsonified = json.loads(response)
        formatted_json = json.dumps(jsonified, sort_keys=True, indent=4)
        response_formatted = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    
    if "/html" in response_type:
        response_formatted = highlight(response, lexers.HtmlLexer(), formatters.TerminalFormatter())
    
    return response_formatted

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="wtf.json", help="File input")
    parser.add_argument("-c", "--colorized", default=True, help="Colored output")
    args = parser.parse_args()
    
    shit = WTF(args.file)
    response = shit.get_response()
    
    if args.colorized:
        response = colorized(response, shit.get_response_type())
    
    print(response)

if __name__ == "__main__":
    main()
