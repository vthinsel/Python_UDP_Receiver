# ----------------------------------------------------------------------------------------------------------------------
# Test tool to receive packed values.
# Assumes packed data is of fixed size.
# ----------------------------------------------------------------------------------------------------------------------

#Check http://forums.codemasters.com/discussion/46726/d-box-and-udp-telemetry-information
#command line to generate traffic : C:\Users\vthinselin\Google Drive\Loisirs\Playseat\Python_UDP_Receiver>python UDPSend_timed.py -s 127.0.0.1 -p 20777 -f f1_2016_ps4.bin

import sys
import struct
import socket

# Configure listener IP & Port for UDP transmission of packed values
udp_ip = "0.0.0.0"
udp_port = 20777

def net_rx(UDP_IP, UDP_PORT):
    # Receive packet from wire
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.bind((UDP_IP, UDP_PORT))
    data, addr = sock.recvfrom(1024)  # receiving from socket
    return data

def displaygear(gear):
    # | car gear | data gear |                             Required to adjust for gear float mapping as shown
    # |    R     |     0     |
    # |    N     |     1     |
    # |    1     |     2     |
    # |    2     |     3     |
    # |    3     |     4     |
    # |    4     |     5     |
    # |    5     |     6     |
    # |    6     |     7     |
    # |    7     |     8     |
    # ------------------------

    if (gear > 1):                                         # Forward gear requires minus adjustment
        gear -=1
        print("Current Gear :%d" % gear)  # print forward gear
    elif (gear == 1):
        print("Current Gear :N")  # print neutral
    elif (gear == 0):
        print("Current Gear :R")  # print reverse
    return

def displaymph(mph):
    print("Current MPH  :%f" % mph)
    return

def receiver():
    fmt = '<' + '70' + 'f'                                 # define structure of packed data
    s = struct.Struct(fmt)                                  # declare structure
    packetCounter = 0
    recordedData = []
    # Infinite receiving loops
    while True:
        rx_data = net_rx(udp_ip, udp_port)
        unpacked_data = s.unpack(rx_data)                  #  unpack data into tuple, requires correct 'fmt'
        displaygear(unpacked_data[33])
        print("Current RPM  :%d" % unpacked_data[37])
        displaymph(unpacked_data[7])
    return

def main():
    receiver()
    return

if __name__ == '__main__':
    main()