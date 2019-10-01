"""
author: yingshaoxo
gmail: yingshaoxo@gmail.com

ls -l /dev/ttyUSB0
sudo usermod -a -G uucp yingshaoxo
sudo chmod a+rw /dev/ttyUSB0
"""
import serial
import binascii
from time import sleep


def bytes_to_hex(a_byte, length=2):
    return str(binascii.hexlify(a_byte))[2:-1]


def hex_to_bytes(hex_string):
    return binascii.unhexlify(hex_string)


def int_to_hex(integer, length=None):
    if length != None:
        hex_string = ('{:0'+str(length)+'X}').format(integer)
    else:
        hex_string = hex(integer)[2:]
        if (len(hex_string) % 2 == 1):
            hex_string = "0" + hex_string
    return hex_string


def hex_to_int(hex_string):
    return int(hex_string, 16)


def int_to_bytes(integer, length=None):
    hex_string = int_to_hex(integer, length)
    return hex_to_bytes(hex_string)


def bytes_to_int(a_byte):
    hex_string = bytes_to_hex(a_byte)
    return hex_to_int(hex_string)


def text_to_hex(text):
    length = len(text) * 2
    bytes_ = binascii.hexlify(text.encode("ascii", "ignore"))
    result = str(bytes_)
    result = result[2:][:-1]
    return result


class MyTransmissionProtocol():
    def __init__(self, port="/dev/ttyUSB0"):
        self.serial = serial.Serial(port, 115200)  # open serial port
        print(self.serial.name)         # check which port was really used
        print('-'*10)

    def write(self, id_, bytes_data):
        # for data less than 256
        hex_string = bytes_to_hex(bytes_data)
        length = len(hex_string)//2
        idle_hex = "00"
        hex_string = idle_hex*3 + int_to_hex(length) + int_to_hex(id_) + hex_string + idle_hex*3
        self.serial.write(hex_to_bytes(hex_string))

    def read(self):
        hex_data = ""
        while 1:
            if self.serial.readable():
                a_byte = self.serial.read(1)
                if bytes_to_hex(a_byte) != "00":
                    length = bytes_to_int(a_byte)
                    while not self.serial.readable():
                        pass
                    a_byte = self.serial.read(1)
                    id_ = bytes_to_int(a_byte)
                    while length > 0:
                        if self.serial.readable():
                            length -= 1
                            a_byte = self.serial.read(1)
                            hex_data += bytes_to_hex(a_byte)
                    return id_, hex_data



my_transmission = MyTransmissionProtocol("/dev/ttyUSB0")

sleep(3)

i = 255
while 1:
    i -= 1

    my_transmission.write(1, hex_to_bytes(text_to_hex(str(i)+"yingshaoxo")))

    if i == 0:
        i = 255
