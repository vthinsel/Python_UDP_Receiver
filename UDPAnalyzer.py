import base64
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
args = parser.parse_args()
HOST = ''  # Symbolic name meaning all available interfaces
HOST = 'localhost'
if args.port != None:
    PORT = int(args.port)
else:
    PORT = 20000
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error as msg:
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
print('Socket bind complete')

# now keep talking with the client
while 1:
    # receive data from client (data, addr)
    d = s.recvfrom(5)
    data = d[0]
    addr = d[1]
    if not data:
        break
    reply = 'OK...' + data
    s.sendto(reply, addr)
    print('Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip())
s.close()

#    print("UDP listening on %s:%s" %(HOST,PORT))
#    server = socketserver.UDPServer((HOST, PORT), MyUDPHandler)
#    server.serve_forever()
