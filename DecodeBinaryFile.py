import struct
import argparse


class BinaryReaderEOFException(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return 'Not enough bytes in file to satisfy read request'


class BinaryReader:
    # Map well-known type names into struct format characters.
    typeNames = {
        'int8': 'b',
        'uint8': 'B',
        'int16': 'h',
        'uint16': 'H',
        'int32': 'i',
        'uint32': 'I',
        'int64': 'q',
        'uint64': 'Q',
        'float': 'f',
        'double': 'd',
        'char': 's'}

    def __init__(self, fileName,offset):
        self.file = open(fileName, 'rb')
        self.file.read(offset)  # Go to the offset in first packet

    def read(self, typeName: object, offset, packetsize) -> object:
        typeFormat = BinaryReader.typeNames[typeName.lower()]
        typeSize = struct.calcsize(typeFormat)
        value = self.file.read(typeSize)
        if typeSize != len(value):
            raise BinaryReaderEOFException
        if packetsize >0:
            self.file.read(packetsize - typeSize) # Go to next packet
        return struct.unpack(typeFormat, value)[0]

    def __del__(self):
        self.file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Analyze binary file')
    parser.add_argument('-f', '--file', help='File to analyze', required=True)
    parser.add_argument('-o', '--offset', help='Offset', required=False)
    parser.add_argument('-p', '--packsetsize', help='Packet size', required=False)
    parser.add_argument('-s', '--samples', help='Number of values to report', required=False)
    parser.add_argument('-t', '--type', help='[int8|uint8|int16|int32|uint32|int64|uint64|float|double|char]', required=True)

    args = parser.parse_args()
    if args.offset is None:
        offset = 0
    else:
        offset = int(args.offset)

    if args.packsetsize is None:
        packsetsize = 0
    else:
        packsetsize = int(args.packsetsize)

    if args.samples is not None:
        samples = int(args.samples)

    binaryReader = BinaryReader(args.file,offset)

    try:
        # packetId = binaryReader.read('uint8')
        # timestamp = binaryReader.read('uint64')
        # secretCodeLen = binaryReader.read('uint32')
        # secretCode = []
        # while secretCodeLen > 0:
        #    secretCode.append(binaryReader.read('uint8'))
        #    secretCodeLen = secretCodeLen - 1
        # print(secretCode)
        while True:
            data = binaryReader.read(args.type, offset, packsetsize)
            print(data)
            if args.samples is not None:
                samples = samples - 1
                if samples < 0:
                    exit()

    except BinaryReaderEOFException:
        # One of our attempts to read a field went beyond the end of the file.
        print
        "Error: File seems to be corrupted."
