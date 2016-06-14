import struct
#import base64
#import binascii
import time
import datetime
import requests
import pickle
#import getopt, sys
import argparse
#import json
import socket
import sys
import os
#import socketserver
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# if __name__ == "__main__":
parser = argparse.ArgumentParser(
    description='Capture UDP packets for further analysis')
parser.add_argument('-p', '--port', help='Port to listen to', required=False)
parser.add_argument('-f', '--file', help='Port to listen to', required=False)
parser.add_argument('-b', '--buffer', help='Host target', required=False)

args = parser.parse_args()
HOST = ''  # Symbolic name meaning all available interfaces
# HOST = "127.0.0.1"
if args.buffer is not None:
    buf = int(args.buffer)
else:
    buf = 1500
if args.port is not None:
    PORT = int(args.port)
else:
    PORT = 5606
if args.file is not None:
    file = args.file
else:
    file = 'udp.bin'
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error as msg:
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
# Bind socket to local host and port
try:
    s.bind((HOST, 5606))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
print('Socket bind complete')

f = open(file, 'wb')
f2 = open(file + '.raw.bin', 'wb')
previousts = datetime.datetime.now()
delta=0
while 1:
    d = s.recvfrom(buf)
    data = d[0]
    addr = d[1]
    if not data:
        break
    ts = datetime.datetime.now()
    delta = ts - previousts
    previousts = datetime.datetime.now()
    previoustime = ('{:%H:%M:%S:%f}'.format(datetime.datetime.now()))
    record = [previoustime, delta, data]
    pickle.dump(record, f)
    f2.write(data)
    print('%s %s %s' % (previoustime, delta, data))
f.close()
f2.close()
