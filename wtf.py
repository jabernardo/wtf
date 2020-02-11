#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 12:07:34 2020

@author: jabernardo
"""

import argparse
import json
import os.path

from lib import WTF, JSONFile
from lib.assert_json import AssertJSON 
import json
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

def authenticate(auth = {}):
    if not "username" in auth:
        auth["username"] = input("Username: ")

    if not "password" in auth:
        auth["password"] = getpass("Password: ")

    return auth

def assert_results(expected, actual_data):
    if not "assert" in expected:
        raise Exception("No tests found")

    try:
        actual_data = json.loads(actual_data)
    except:
        raise Exception("Response is not supported for assert.")

    assert_obj = AssertJSON(expected["assert"], actual_data)

    results = assert_obj.get_results()
    total_tests = len(results)
    total_failed = 0

    for result in results:
        if result['status'] == 'FAILED':
            total_failed += 1
        
            print(f"{'Object Key:':<20} {fore.YELLOW}{result['key']} {fore.LIGHT_GRAY}{back.RED}{style.BOLD}({result['status']}){style.RESET}")
            print(f"{'Expected value:':<20} {fore.GREEN}{result['expected_val']}{style.RESET}")
            print(f"{'Actual value:':<20} {fore.RED}{result['actual_val']}{style.RESET}")
            print(f"{fore.DARK_GRAY}================================================================================{style.RESET}")

    if total_failed:
        print(f"{fore.RED}{total_failed} failed {fore.LIGHT_GRAY}out of {fore.GREEN}{total_tests}{style.RESET}\n")
    else:
        print(f"{style.BOLD}{back.GREEN}{fore.LIGHT_GRAY}ALL GOOD!{style.RESET}\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="wtf.json", help="File input")
    parser.add_argument("-a", "--test", action="store_true", default=False, help="Assert results")
    parser.add_argument("-r", "--raw", action="store_true", default=False, help="Colored output")
    args = parser.parse_args()
    
    try:
        if not os.path.isfile(args.file):
            raise Exception("No input file (wtf.json) ")

        data = JSONFile(args.file).get_data()

        if "authentication" in data:
            if type(data["authentication"]) == dict:
                data["authentication"] = authenticate(data["authentication"])
            else:
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

        if args.test:
            assert_results(data, shit.get_response())
        else:
            print(f'{fore.LIGHT_GREEN}{style.BOLD}{request_data["label"]}{style.RESET}')
            print(f'{style.BOLD}{"URL:":<20} {fore.BLUE}{request_data["url"]}{style.RESET}')
            print(f'{style.BOLD}{"METHOD:":<20} {fore.BLUE}{request_data["method"]}{style.RESET}')
            print(f'{style.BOLD}{"STATUS:":<20} {status_color}{response_data.status} {response_data.reason}{style.RESET}')
            print(f'{style.BOLD}HEADERS: {fore.BLUE}\n{response_data.headers}{style.RESET}')
            print(f'{style.BOLD}DATA:\n{response}{style.RESET}')

    except Exception as err:
        print(f'{back.RED}{style.BOLD}{err}{style.RESET}\n')

if __name__ == "__main__":
    main()
