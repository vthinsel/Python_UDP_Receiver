import base64
import binascii
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

# if __name__ == "__main__":
parser = argparse.ArgumentParser(
    description='Capture UDP packets for further analysis')
parser.add_argument('-p', '--port', help='Port to listen to', required=False)
parser.add_argument('-f', '--file', help='Port to listen to', required=False)
parser.add_argument('-b', '--buffer', help='Host target', required=False)

args = parser.parse_args()
HOST = ''  # Symbolic name meaning all available interfaces
# HOST = "127.0.0.1"
if args.buffer != None:
    buf = int(args.buffer)
else:
    buf = 1500
if args.port != None:
    PORT = int(args.port)
else:
    PORT = 5606
if args.file != None:
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
f2 = open(file+'.ts','wb')
previoustime = datetime.datetime.now()
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(buf)
    data = d[0]
    addr = d[1]
    if not data:
        break
    delta = datetime.datetime.now() - previoustime
    previoustime = datetime.datetime.now()
    udptime = ('{:%H:%M:%S:%f}'.format(datetime.datetime.now()))

    print('%s %s %s' % (udptime, delta, data))
    # f.write(bytes(udptime))
    #f.write(str.encode(str(delta))+data)
    f.write(data)
    f2.write(str.encode(str(delta)))
s.close()
f.close()
f2.close()