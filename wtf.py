#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WTF! Console POST

- Send request using json files
- Assert results from response (only json is currently supported)

@author: jabernardo
@email: 4ldrich@protonmail.com
"""

__version__ = "0.1.0"

import argparse
import json
import os.path

from lib import WTF, JSONFile, ArgumentsParser
import lib.validators as validators
from lib.assert_json import AssertJSON 
from getpass import getpass
from pygments import highlight, lexers, formatters
from colored import fore, back, style

from lowder import Lowder, LOADERS

def colorized(response, response_type):
    """Colorized responses output

    \nArguments:\n
    `response` (str) -- Response string\n
    `response_type` (str) -- Content-type\n

    \nReturns:\n
    `None`
    """

    response_formatted = response
    
    # Content-types from response headers
    # todo:
    #  - Add more types to support see supported lexers by pygment
    if "application/json" in response_type:
        jsonified = json.loads(response)
        formatted_json = json.dumps(jsonified, sort_keys=True, indent=4)
        response_formatted = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    
    if "text/html" in response_type:
        response_formatted = highlight(response, lexers.HtmlLexer(), formatters.TerminalFormatter())
    
    return response_formatted

def authenticate(auth = {}):
    """Validate authentication node

    \nArguments:\n
    `auth` (dict) -- Authentication node\n

    \nReturns:\n
    `None`
    """

    # As for username
    if not "username" in auth:
        auth["username"] = input("Username: ")

    # and password if not set
    if not "password" in auth:
        auth["password"] = getpass("Password: ")

    return auth

def assert_results(expected, actual_data):
    """Assert results\n

    \nArguments:\n
    `expected` (dict) -- Expected json output\n
    `actual_data` (dict) -- Actual response json

    \nReturns:\n
    `str`
    """

    # Validate if assertions are specified on the json file
    if not "assert" in expected:
        raise Exception("No tests found")

    try:
        actual_data = json.loads(actual_data)
    except:
        # Assertions only supports json responses
        raise Exception("Response is not supported for assert.")

    # Call validation class
    assert_obj = AssertJSON(expected["assert"], actual_data)

    results = assert_obj.get_results()
    total_tests = len(results)
    total_failed = 0
    report = ""

    for result in results:
        if result['status'] == 'FAILED':
            total_failed += 1
        
            report += f"{'Object Key:':<20} {fore.YELLOW}{result['key']} {fore.LIGHT_GRAY}{back.RED}{style.BOLD}({result['status']}){style.RESET}"
            report += f"{'Expected value:':<20} {fore.GREEN}{result['expected_val']}{style.RESET}"
            report += f"{'Actual value:':<20} {fore.RED}{result['actual_val']}{style.RESET}"
            report += "{fore.DARK_GRAY}================================================================================{style.RESET}"

    if total_failed:
        report += f"{fore.RED}{total_failed} failed {fore.LIGHT_GRAY}out of {fore.GREEN}{total_tests}{style.RESET}\n"
    else:
        report += f"{style.BOLD}{back.GREEN}{fore.LIGHT_GRAY}ALL GOOD!{style.RESET}\n"
        
    return report

def console(source, formatted_response = True):
    """Console POST\n

    \nArguments:\n
    `source` (WTF) -- Instance of WTF\n
    `formatted_response` (bool=True) -- Show formatted output

    \nReturns:\n
    `str`
    """

    if not isinstance(source, WTF):
        raise Exception("Source must be an instance of WTF")

    response = source.get_response()

    if formatted_response:
        response = colorized(response, source.get_response_type())
    
    request_data = source.get_request_data()
    response_data = source.get_response_raw()
    
    status_color = fore.GREEN

    if response_data.status != 200:
        status_color = fore.RED

    report = ""
    report += f'{fore.LIGHT_GREEN}{style.BOLD}{request_data["label"]}{style.RESET}\n'
    report += f'{style.BOLD}{"URL: ":<20} {fore.BLUE}{request_data["url"]}{style.RESET}\n'
    report += f'{style.BOLD}{"METHOD: ":<20} {fore.BLUE}{request_data["method"]}{style.RESET}\n'
    report += f'{style.BOLD}{"STATUS: ":<20} {status_color}{response_data.status} {response_data.reason}{style.RESET}\n'
    report += f'{style.BOLD}HEADERS : {fore.BLUE}\n{response_data.headers}{style.RESET}\n'
    report += f'{style.BOLD}DATA: \n{response}{style.RESET}\n'
    report += f'{style.BOLD}RESPONSE TIME: {fore.BLUE}{source.get_profile("time")}{style.RESET}\n'
    return report

def call_lowder(loader, data):
    """Call WTF thread\n
    \nArguments:\n
    `loader` (Lowder) -- Instance of Lowder\n
    `data` (dict) -- WTF Configuration data\n
    
    \nReturns:\n
    `object`
    """
    try:
        result = WTF(data)
    except Exception as ex:
        return ex
    finally:
        loader.stop()
    
    return result

def call_assert(loader, expected, actual):
    """Call WTF thread\n
    \nArguments:\n
    `loader` (Lowder) -- Instance of Lowder\n
    `expected` (dict) -- WTF Configuration assert data\n
    `actual` (dict) -- JSON response data\n
    
    \nReturns:\n
    `object`
    """
    try:
        result = assert_results(expected, actual)
    except Exception as ex:
        return ex
    finally:
        loader.stop()
        
    return result

def get_args():
    """Parse arguments"""

    parser = argparse.ArgumentParser()
    # positional file argument
    parser.add_argument("source", nargs="?", default="wtf.json", help="File input")
    # wtf -a or wtf --test
    ## Run assert tests
    parser.add_argument("-a", "--test", action="store_true", default=False, help="Assert results")
    # wtf -f {file} -r or wtf -f {file} --raw
    ## Show raw output only
    parser.add_argument("-r", "--raw", action="store_true", default=False, help="Colored output")

    # In-line data collection params
    parser.add_argument("-m", "--method", default="GET", help="In-line request: http request")
    parser.add_argument("-l", "--login", action="store_true", default=False, help="In-line request: login")
    parser.add_argument("-d", "--data", action="append", nargs='*', default=None, help="In-line request: data")
    parser.add_argument("-H", "--header", action="append", nargs='*', default=None, help="In-line request: header")
    parser.add_argument("-o", "--out", default=None, help="In-line request: save to json")

    # Show version
    parser.add_argument("-v", "--version", default=False, action="store_true", help="Show application version")

    return parser.parse_args()

def json_dump(file_name, data):
    """JSON Dump\n
    \nArguments:\n
    `file_name` (str) -- Dumps filename\n
    `data` (dict) -- Data to be written\n
    \nThrows:\n
    `Exception`
    """
    try:
        with open(file_name, "w") as json_out:
            json_out.write(json.dumps(data))
            json_out.close()
    except Exception as ex:
        raise ex

def show_version():
    print(f'Version: {__version__}\n')

def main():
    """Application entry-point
    """

    # Dict data
    data = {}

    # Parse arguments
    args = get_args()

    if args.version:
        return show_version()
    
    try:
        if not os.path.isfile(args.source) and not validators.is_url(args.source):
            raise Exception("No input file (wtf.json) or valid url given.")

        if validators.is_url(args.source):
            data = ArgumentsParser(args).items()

            if args.out:
                json_dump(args.out, data)
        else:
            data = JSONFile(args.source).get_data()

        if "authentication" in data:
            if type(data["authentication"]) == dict:
                data["authentication"] = authenticate(data["authentication"])
            else:
                data["authentication"] = authenticate()

        load_screen = Lowder()
        shit = load_screen.start("Fetching...", lambda: call_lowder(load_screen, data), LOADERS['dots'])

        if isinstance(shit, Exception):
            raise shit
                
        if args.test:
            report = load_screen.start("Loading test results...", lambda: call_assert(load_screen, data, shit.get_response()), LOADERS['dots'])
            print(report)
        else:
            print(console(shit, not args.raw))

    except Exception as err:
        print(f'{back.RED}{style.BOLD}{err}{style.RESET}\n')

if __name__ == "__main__":
    main()
