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
import json


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

def hex_to_text(hex_string):
    bytes_data = hex_to_bytes(hex_string)
    text = bytes_data.decode("ascii", "ignore")
    return text

class MyTransmissionProtocol():
    def __init__(self, port="/dev/ttyUSB0"):
        self.serial = serial.Serial(port, 115200, timeout=0.1, write_timeout=0.1)  # open serial port
        print(self.serial.name)         # check which port was really used
        print('-'*10)
        self.idle_hex = "00"*3

    def write(self, bytes_data):
        # for data less than 256
        hex_string = bytes_to_hex(bytes_data)
        length = len(hex_string)//2 - 1  # one byte(hex) can only express 0-255
        hex_string = self.idle_hex + int_to_hex(length) + hex_string
        self.serial.write(hex_to_bytes(hex_string))

    def read(self):
        hex_data = ""
        previous_hex_list = []
        max_attempts = 10
        while 1:
            max_attempts -= 1
            if (max_attempts < 0):
                return None

            if self.serial.readable():
                a_byte = self.serial.read(1)
                if a_byte != b"":  # timeout
                    previous_hex_list.append(bytes_to_hex(a_byte))
                    previous_hex_list = previous_hex_list[-len(self.idle_hex):]
                    if (bytes_to_hex(a_byte) != "00") and all(map(lambda x: x == "00", previous_hex_list[:-1])):
                        length = bytes_to_int(a_byte)
                        while not self.serial.readable():
                            pass
                        while length >= 0:  # the length is in 0 and 255
                            if self.serial.readable():
                                length -= 1
                                a_byte = self.serial.read(1)
                                hex_data += bytes_to_hex(a_byte)
                        return hex_to_bytes(hex_data)

    def check_to_sync(self):
        # print("checking...")
        #print("writing check...")
        self.write(b"check")
        while 1:
            #print("getting reply...")
            reply = self.read()
            if reply == b"yes":
                break
            elif reply == b"no":
                pass
            elif reply == None:
                #print("writing check...")
                self.write(b"check")

    def reply_to_sync(self):
        # print("replying...")
        while 1:
            #print("getting check...")
            msg = self.read()
            if msg == b"check":
                #print("writing reply...")
                self.write(b"yes")
                break
            else:
                #print("writing reply...")
                self.write(b"no")

    def write_safely(self, bytes_data):
        self.check_to_sync()
        self.write(bytes_data)

    def read_safely(self):
        self.reply_to_sync()
        return self.read()

    def write_large_data(self, bytes_data):
        def to_chunks(data, length):
            return [data[0+i:length+i] for i in range(0, len(data), length)]
        #print("writting head...")
        self.write_safely(b"--head--")
        for index, byte in enumerate(to_chunks(bytes_data, 256)):
            #print("writting trunk{}...".format(str(index)))
            self.write_safely(byte)
        #print("writting tail...")
        self.write_safely(b"--tail--")

    def read_large_data(self):
        data = b""
        i = 0
        while 1:
            chunk = self.read_safely()
            if chunk == b"--head--":
                while 1:
                    chunk = self.read_safely()
                    if chunk != b"--tail--":
                        i += 1
                        data += chunk
                    else:
                        return data

    def write_json(self, dictionary):
        text = json.dumps(dictionary)
        hex_string = text_to_hex(text)
        bytes_data = hex_to_bytes(hex_string)
        self.write_large_data(bytes_data)

    def read_json(self):
        bytes_data = self.read_large_data()
        hex_string = bytes_to_hex(bytes_data)
        text = hex_to_text(hex_string)
        dictionary = json.loads(text)
        return dictionary
