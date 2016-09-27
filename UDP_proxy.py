import datetime
import argparse
import socket
import sys
import signal

def closeapp(nbpkt, secs):
    print('%s packets forwarded in %s seconds. Stopping forward' % (nbpkt, secs))
    s.close()
    sys.exit(0)

def signal_handler(signal, frame):
    closeapp(udppackets, (datetime.datetime.now() - starttime).seconds)

signal.signal(signal.SIGINT, signal_handler)
parser = argparse.ArgumentParser(
    description='Capture UDP packets for further analysis and playback')
parser.add_argument('-p', '--port', help='Port to listen to', required=True)
parser.add_argument('-b', '--buffer', help='Host target', required=False)
parser.add_argument('-s1', '--server1', help='Host 1 target', required=True)
parser.add_argument('-p1', '--port1', help='Host 1 port', required=True)
parser.add_argument('-s2', '--server2', help='Host 2 target', required=False)
parser.add_argument('-p2', '--port2', help='Host 2 port', required=False)
parser.add_argument('-s3', '--server3', help='Host 2 target', required=False)
parser.add_argument('-p3', '--port3', help='Host 2 port', required=False)
args = parser.parse_args()
HOST = ''  # Symbolic name meaning all available interfaces
# HOST = "127.0.0.1"

if args.buffer is not None:
    buf = int(args.buffer)
else:
    buf = 1500

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Socket created')
except socket.error as msg:
    print('Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
# Bind socket to local host and port
try:
    s.bind((HOST, int(args.port)))
    print('Socket bind complete on port %s.' % (args.port))
    print('Press Ctrl+C to stop capturing')
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
s.setblocking(0)

server1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr1 = (args.server1, int(args.port1))
print('Socket created on %s port %s' % (addr1))

server2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
addr2 = (args.server2, int(args.port2))
print('Socket created on %s port %s' % (addr2))

if args.server3 is not None:
    server3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr3 = (args.server3, int(args.port3))
    print('Socket created on %s port %s' % (addr3))


while 1:
    try:
        d = s.recvfrom(buf)
    except BlockingIOError:
        continue
    data = d[0]
    addr = d[1]
    print("%s - Got %s bytes from %s " %(datetime.datetime.now(),len(data),addr))
    server1.sendto(data, addr1)
    server2.sendto(data, addr2)
    if args.server3 is not None:
        server3.sendto(data, addr3)

