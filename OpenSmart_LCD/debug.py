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


def int_to_byte(integer):
    hex_string = '{:02x}'.format(integer)
    a_byte = binascii.unhexlify(hex_string)
    return a_byte


def byte_to_int(a_byte):
    hex_string = binascii.hexlify(a_byte)
    integer = int(hex_string, 16)
    return integer


def byte_to_string(a_byte, length=2):
    return format(byte_to_int(a_byte), "02X").zfill(length)


ser = serial.Serial('/dev/ttyUSB0', 115200)  # open serial port
# ser = serial.Serial('/dev/ttyUSB0', 9600)  # open serial port
print(ser.name)         # check which port was really used

start = 0
i = 0
string = ""
print()
print("7e036f6bef")
print('-'*10)
while 1:
    if ser.writable():
        #ser.write(int_to_byte(i))  # write one byte
        ser.write(bytes.fromhex("7e036f6bef"))
        pass
    if ser.readable():
        a_byte = ser.read(1)  # read one byte
        print(a_byte.hex())
        #print(byte_to_int(a_byte))
        if (a_byte.hex() == "7e"):
            start = 1
        if (start == 1):
            string += a_byte.hex()
            if a_byte.hex() == "ef":
                print(string)
                if (string != "7e042007e0ef"):
                    pass
                    #break
                start = 0
                string = ""

    i += 1
    if i > 255:
        i = 0
