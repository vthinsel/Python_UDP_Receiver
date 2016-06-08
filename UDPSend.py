import base64
import datetime
import requests
import getopt, sys
import argparse
import json
import socket
import sys
import socketserver
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

parser = argparse.ArgumentParser(
    description='Send  UDP file captured previously')
parser.add_argument('-p', '--port', help='Port to listen to', required=True)
parser.add_argument('-f', '--file', help='File to send', required=True)
parser.add_argument('-s', '--server', help='Host target', required=True)
parser.add_argument('-b', '--buffer', help='Host target', required=False)
args = parser.parse_args()
HOST = args.server
PORT = int(args.port)
file_name = args.file
if args.buffer != None:
    buf  = int(args.buffer)
else:
    buf = 1500
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error as msg:
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
# Bind socket to local host and port
addr = (HOST,PORT)
f=open(file_name,"rb")
data = f.read(buf)
while (data):
    if(s.sendto(data,addr)):
        print ("sending ...")
        data = f.read(buf)
s.close()
f.close()
