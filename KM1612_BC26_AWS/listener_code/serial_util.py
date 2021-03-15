from binascii import crc32, hexlify
from typing import NamedTuple
from serial import Serial
from struct import calcsize, pack, unpack

CMD_OK = 0
CMD_ERROR = 1
CMD_PRINTF = 2
CMD_ENTER_COMM = 3
CMD_PUBLIC_ID_GET = 5
CMD_PUBLIC_ID_REPORT = 6
CMD_INIT_REQUEST = 7
CMD_INIT = 8
CMD_GET_N = 9
CMD_POINT = 10

HEADER_FORMAT = '<II'
HEADER_SIZE = calcsize(HEADER_FORMAT)
CHECKSUM_SIZE = 1
GARBAGE_SIZE = 1
PREAMBLE = bytes([0xC9, 0x1E, 0xB1, 0x81])
PREAMBLE_SIZE = len(PREAMBLE)


def read_preamble(ser: Serial):
    preamble = ser.read(PREAMBLE_SIZE)
    while preamble != PREAMBLE:
        preamble = preamble[1:PREAMBLE_SIZE] + ser.read(1)


class SerialHeader(NamedTuple):
    tag: int
    payload_len: int

    @property
    def bytes(self) -> bytes:
        return pack(HEADER_FORMAT, self.tag, self.payload_len)


class SerialCommand:
    def __init__(self, header: SerialHeader, payload: bytes):
        self.header = header
        self.payload = payload or b''
        checksum = crc32(self.header.bytes + self.payload)
        self.crc = pack('<I', checksum)[:CHECKSUM_SIZE]

    @property
    def tag(self) -> int:
        return self.header.tag

    @property
    def bytes(self) -> bytes:
        return PREAMBLE + self.header.bytes + self.payload + self.crc


def read_header(ser) -> SerialHeader:
    b = ser.read(HEADER_SIZE)
    tag, payload_len = unpack(HEADER_FORMAT, b)
    return SerialHeader(tag, payload_len)


def read_command(ser):
    read_preamble(ser)
    header = read_header(ser)
    payload = ser.read(header.payload_len) if header.payload_len else None
    crc = ser.read(CHECKSUM_SIZE)
    cmd = SerialCommand(header, payload)
    if crc != cmd.crc:
        raise Exception('CRC check failed')
    print('cmd read from module:', hexlify_bytes(cmd.bytes))
    return cmd


def write_command(ser, cmd):
    b = cmd.bytes
    print('cmd sent to module:', hexlify_bytes(b))
    ser.write(b)
    ser.write(bytes(GARBAGE_SIZE))


def hexlify_bytes(b: bytes) -> str:
    s = hexlify(b).decode()
    return ','.join([f'0x{s[i*2: i*2+2]}' for i in range(len(s) // 2)])
