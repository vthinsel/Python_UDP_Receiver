import argparse
import socket
import sys
import pickle
import time

parser = argparse.ArgumentParser(
    description='Send UDP file captured previously using UDPReceive.py')
parser.add_argument('-p', '--port', help='Port to listen to', required=True)
parser.add_argument('-f', '--file', help='File to send', required=True)
parser.add_argument('-s', '--server', help='Host target', required=True)
parser.add_argument('-b', '--buffer', help='Buffer size', required=False)
args = parser.parse_args()
HOST = args.server
PORT = int(args.port)
file_name = args.file
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
addr = (HOST, PORT)
f = open(file_name, "rb")
try:
    record = pickle.load(f)
except (EOFError, pickle.UnpicklingError):
    print("Malformed file. Make sure the file was ceated using UDPReceive.py")
    f.close()
    s.close()
    exit()
while record:
    if s.sendto(record[2], addr):
        print("sending timestamp %s with delay %s " % (record[0], record[1]) )
    try:
        record = pickle.load(f)
        time.sleep(record[1].total_seconds()) #convert to seconds
    except (EOFError, pickle.UnpicklingError):
        break
f.close()
