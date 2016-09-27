import datetime
import pickle
import argparse
import socket
import sys
import signal
import time

def closeapp(nbpkt,secs):
    print('%s packets captured in %s seconds. Stopping capture' % (nbpkt, secs))
    f.flush()
    f2.flush()
    f.close()
    f2.close()
    s.close()
    sys.exit(0)

def signal_handler(signal, frame):
    closeapp(udppackets, (datetime.datetime.now()-starttime).seconds)

signal.signal(signal.SIGINT, signal_handler)
parser = argparse.ArgumentParser(
    description='Capture UDP packets for further analysis and playback')
parser.add_argument('-p', '--port', help='Port to listen to', required=True)
parser.add_argument('-f', '--file', help='File to write data to', required=False)
parser.add_argument('-b', '--buffer', help='Buffer size', required=False)
parser.add_argument('-c', '--count', help='Stop capture after x packets', required=False)
parser.add_argument('-s', '--seconds', help='Stop capture after x seconds', required=False)

args = parser.parse_args()
HOST = ''  # Symbolic name meaning all available interfaces
# HOST = "127.0.0.1"
if args.buffer is not None:
    buf = int(args.buffer)
else:
    buf = 1500
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
    s.bind((HOST, int(args.port)))
    print('Socket bind complete on port %s. Output file: %s and %s' % (args.port, file, file + '.raw'))
    print('Press Ctrl+C to stop capturing')
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
s.setblocking(0)
f = open(file, 'wb')
f2 = open(file + '.raw', 'wb')
previousts = datetime.datetime.now()
starttime = datetime.datetime.now()
delta = 0
udppackets = 0

while 1:
    ts = datetime.datetime.now()
    if args.count is not None and udppackets >= int(args.count):
        closeapp(udppackets, (ts - starttime).seconds)
    if args.seconds is not None and (ts - starttime).seconds >= int(args.seconds):
        closeapp(udppackets, (ts - starttime).seconds)
    try:
        d = s.recvfrom(buf)
    except BlockingIOError:
        continue
    data = d[0]
    addr = d[1]
    #if not data:
    #    break
    ts = datetime.datetime.now()
    delta = ts - previousts
    previousts = datetime.datetime.now()
    previoustime = ('{:%H:%M:%S:%f}'.format(datetime.datetime.now()))
    record = [previoustime, delta, data]
    pickle.dump(record, f)
    f2.write(data)
    udppackets = udppackets + 1
    print('%s %s ' % (previoustime, delta))
f.close()
f2.close()
