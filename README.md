# Python_UDP_Receiver - Made with Python 3 

This small repository contains several UDP tools used to capture/replay UDP data. This is usefull when making
applications that require incoming UDP data processing and when this data is not so easy to reproduce. This is true
especially for games that send telemetry data using UDP, so the data is used for applicatiosn managign dashboards,
motion simulation, etc. Developping is much more easy this way as the stimuli is easily reproducible
Timing is also very important to reproduce the application behavior, so each time a UDP packet is received a timestamp
is associated so the replay is accurate with timing information

4 main tools are available :
- The UDP receiver UDPReceive.py that is used to capture the incoming UDP data on a given port. This tool generates
 2 output files, based on the file name provided with the argument -f: a raw file with the UDP data unprocessed (.raw
 suffix added), and another file in a compressed format that includes timing data which is used by the playback tool
 You can specify a maximum number of UDP packets to capture and/or a maximum time in seconds to capture UDP packets

- The UDP raw sender UDPSend_raw.py that sends a raw UDP file captured as fast as it can to a given host/port.

- The "advanced" UDP sender UDPSend_timed which sends the captured UDP data including the timing of the data,
 reflecting the original UDP flow

- The UDP_proxy which you can use in case you need to replicate udp data towards several destinations (upto 3)

A sample UDP stream from ProjectCars is included as reference.

In addition, the DecodeBianryFile.py can be of some help to figure out the raw UDP frame : you give the packet size,
the offset and the data type and you will see the values. On a dirt ralye UDP stream, you can see the speed in m/s 
with the following command:
python DecodeBinaryFile.py -f DirtRallye.raw.bin -t float -p 264 -o 28
(packet size is 264, and speed offset is at 28)
