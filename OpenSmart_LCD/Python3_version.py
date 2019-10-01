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
import random


#DEBUG = False
DEBUG = True


def int_to_byte(integer, length=2):
    hex_string = '{:02X}'.format(integer)
    ok = 0
    while ok == 0:
        try:
            padding_hex = hex_string.zfill(length)
            a_byte = binascii.unhexlify(padding_hex)
            ok = 1
        except Exception as e:
            # print(e)
            length += 2
    return a_byte


def byte_to_int(a_byte):
    hex_string = binascii.hexlify(a_byte)
    integer = int(hex_string, 16)
    return integer


def byte_to_string(a_byte, length=2):
    return format(byte_to_int(a_byte), "02X").zfill(length)
    # return '{0:02X}'.format(byte_to_int(a_byte))


def hex_to_bytes(a_hex_string):
    return bytes.fromhex(a_hex_string)


def text_to_hex(text):
    length = len(text)*2
    bytes_ = binascii.hexlify(text.encode("ascii", "ignore"))
    result = str(bytes_)
    result = result[2:][:-1]
    return result


class SmartOpen_LCD():
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=0.1, write_timeout=0.1)  # open serial port
        print()
        print('-'*20)
        print(self.serial.name)         # check which port was really used
        print('-'*20)
        print()

        self.color_table = {
            "black": "0000",
            "blue": "001F",
            "red": "F800",
            "green": "07E0",
            "cyan": "07FF",
            "magenta": "F81F",
            "yellow": "FFE0",
            "white": "FFFF",
        }

        self.wait(1.5)
        self.set_baud()

    def wait(self, time=1):
        sleep(time)

    def reset(self):
        self.write_command("7E0205EF")
        self.wait(6)

    def set_baud(self):
        baud_index = byte_to_string(int_to_byte(4))
        self.write_command(f"7E0340{baud_index}EF")

    def read_feedback_signal(self):
        bytes_string = ""
        start = 0
        attempts = 6
        while attempts:
            attempts -= 1
            #print(attempts)
            if self.serial.readable():
                a_byte = self.serial.read(1)
                if a_byte:
                    byte_string = byte_to_string(a_byte)
                    #print(f"read: {byte_string}")
                    if byte_string == "7E":
                        start = 1
                    if start == 1:
                        bytes_string += byte_string
                        if byte_string == "EF":
                            return byte_to_string

    def wait_for_command_to_be_executed(self):
        if self.read_feedback_signal() == "7E036F6BEF":
            return True
        else:
            return False

    def write_command(self, hex_string):
        if self.serial.writable():
            self.serial.write(hex_to_bytes(hex_string))
            if DEBUG:
                print(f"write: {hex_string}")
        self.wait_for_command_to_be_executed()

    def set_blacklight(self, brightness):
        brightness_hex = byte_to_string(int_to_byte(brightness))
        self.write_command(f"7E0306{brightness_hex}EF")

    def fill_screen(self, color="white"):
        if color in self.color_table.keys():
            color = self.color_table[color]
        self.write_command(f"7E0420{color}EF")

    def draw_pixel(self, x, y, color="black"):
        if color in self.color_table.keys():
            color = self.color_table[color]
        x = byte_to_string(int_to_byte(x), 4)
        y = byte_to_string(int_to_byte(y), 4)
        self.write_command(f"7E0821{x}{y}{color}EF")

    def draw_rectangle(self, x, y, width, height, color="black"):
        if color in self.color_table.keys():
            color = self.color_table[color]
        x = byte_to_string(int_to_byte(x), 4)
        y = byte_to_string(int_to_byte(y), 4)
        width = byte_to_string(int_to_byte(width), 4)
        height = byte_to_string(int_to_byte(height), 4)
        self.write_command(f"7E0C26{x}{y}{width}{height}{color}EF")

    def write_string(self, x, y, text):
        # set cursor
        self.write_command(f"7E060100000000EF")

        # set Text color
        self.write_command(f"7E0402f800EF")

        # set text size
        self.write_command(f"7E030302EF")

        def chunkstring(string, length):
            return [string[0+i:length+i] for i in range(0, len(string), length)]

        for i in range(y*2):
            # new line
            self.write_command(f"7E0210EF")
            self.write_command(f"7E0210EF")

        text_list = chunkstring(text, 5)
        for index, text in enumerate(text_list):
            text = text_to_hex(text.ljust(5))
            self.write_command(f"7E0711{text}EF")

color_table = {
    "black": "0000",
    "blue": "001f",
    "red": "f800",
    "green": "07e0",
    "cyan": "07ff",
    "magenta": "f81f",
    "yellow": "ffe0",
    "white": "ffff",
}

lcd = SmartOpen_LCD()

# lcd.reset()
lcd.set_blacklight(150)
#color = random.choice(list(lcd.color_table.keys()))
color = lcd.color_table['white']
lcd.fill_screen(color)

#""
# 80x80 points
#an_image[(y * 16) + x]
width = 240
height = 240
box_length = width // 16
for y in range(16):
    for x in range(16):
        color = random.choice(list(lcd.color_table.keys()))
        box_x = x * box_length
        box_y = y * box_length
        lcd.draw_rectangle(box_x, box_y, box_length, box_length, color=color)
        exit()
#""

"""
### write string
lcd.write_string(0, 0, "Hi, i'm yingshaoxo")
lcd.write_string(0, 1, "The greatest man in this world")
lcd.write_string(0, 2, "Do you love me?")
lcd.write_string(0, 3, "I guess yes")
"""

"""
### draw a squre
height = 240
width = 320
for y in range(height):
    color = random.choice(list(lcd.color_table.keys()))
    print(str(y/height), color)
    for x in range(width):
        if x < width//4:
            if y < height//4:
                lcd.draw_pixel(x, y, color)
"""

"""
### change screen color
while 1:
    for color in color_table.keys():
        lcd.fill_screen(color)
        lcd.wait(0.5)
"""
