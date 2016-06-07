import base64
import requests
import getopt,sys
import argparse
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def usage():
    '''
    Usage goes here
-c 10.102.5.110 -p 9070 -a 3.7 -t TIPGTest -U restadmin -P restadmin -n "Python Test" -i 1.2.3.4,1.2.3.5    '''

def main():
    parser = argparse.ArgumentParser(
        description='Capture UDP packets and anlyze them')
    parser.add_argument('-p', '--port', help='LoadBalancer Management REST port', required=True)
    args = parser.parse_args()

if __name__ == "__main__":
    main()
