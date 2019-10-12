# find_black_lines - By: yingshaoxo - Wed Oct 2 2019

# 注意：线条检测是通过使用霍夫变换完成的：
# http://en.wikipedia.org/wiki/Hough_transform
# 请阅读以上关于“theta”和“rho”的更多信息。

# find_lines（）找到无限长度的线。使用find_line_segments（）
# 来查找非无限线。
import pyb
import ubinascii
import utime
import random


import time
import image
import sensor

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # grayscale is faster
# sensor.set_pixformat(sensor.GRAYSCALE)  # grayscale is faster
sensor.set_framesize(sensor.QQVGA)  # QVGA: 320x240, QQVGA: 160x120
sensor.skip_frames(time=2000)

enable_lens_corr = False  # True  # turn on for straighter lines...

# for getting screen resolution
screen_width = sensor.width()
screen_height = sensor.height()


def bytes_to_hex(a_byte):
    return str(ubinascii.hexlify(a_byte))[2:-1]


def hex_to_bytes(hex_string):
    return ubinascii.unhexlify(hex_string)


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
    length = len(text)*2
    bytes_ = ubinascii.hexlify(text.encode("ascii", "ignore"))
    result = str(bytes_)
    result = result[2:][:-1]
    return result


class SmartOpen_LCD():
    def __init__(self):
        self.serial = pyb.UART(1, 115200, timeout=0)  # open serial port

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
        self.set_blacklight(150)
        self.fill_screen(lcd.color_table["white"])

    def wait(self, time=1):
        utime.sleep_ms(int(time * 1000))

    def reset(self):
        self.write_command("7E0205EF")
        self.wait(6)

    def set_baud(self):
        baud_index = int_to_hex(4)
        self.write_command("7E0340{baud_index}EF".format(baud_index=baud_index))

    def read_feedback_signal(self):
        bytes_string = ""
        start = 0
        attempts = 6
        while attempts:
            attempts -= 1
            # print(attempts)
            if self.serial.any():
                a_byte = self.serial.read(1)
                byte_string = bytes_to_hex(a_byte)
                #print(f"read: {byte_string}")
                if byte_string == "7E":
                    start = 1
                if start == 1:
                    bytes_string += byte_string
                    if byte_string == "EF":
                        return bytes_to_hex
            else:
                self.wait(0.1)

    def wait_for_command_to_be_executed(self):
        if self.read_feedback_signal() == "7E036F6BEF":
            return True
        else:
            return False

    def write_command(self, hex_string):
        self.serial.write(hex_to_bytes(hex_string))
        self.wait_for_command_to_be_executed()

    def set_blacklight(self, brightness):
        brightness_hex = int_to_hex(brightness)
        self.write_command("7E0306{brightness_hex}EF".format(brightness_hex=brightness_hex))

    def fill_screen(self, color="white"):
        if color in self.color_table.keys():
            color = self.color_table[color]
        self.write_command("7E0420{color}EF".format(color=color))

    def draw_pixel(self, x, y, color="black"):
        if color in self.color_table.keys():
            color = self.color_table[color]
        x = int_to_hex(x, 4)
        y = int_to_hex(y, 4)
        self.write_command("7E0821{x}{y}{color}EF".format(x=x, y=y, color=color))

    def draw_line(self, x0, y0, x1, y1, color="black"):
        if color in self.color_table.keys():
            color = self.color_table[color]
        x0 = int_to_hex(x0, 4)
        y0 = int_to_hex(y0, 4)
        x1 = int_to_hex(x1, 4)
        y1 = int_to_hex(y1, 4)
        self.write_command("7E0C24{x0}{y0}{x1}{y1}{color}EF".format(x0=x0, y0=y0, x1=x1, y1=y1, color=color))

    def draw_rectangle(self, x, y, width, height, color="black"):
        if color in self.color_table.keys():
            color = self.color_table[color]
        x = int_to_hex(x, 4)
        y = int_to_hex(y, 4)
        width = int_to_hex(width, 4)
        height = int_to_hex(height, 4)
        self.write_command("7E0C26{x}{y}{width}{height}{color}EF".format(x=x, y=y, width=width, height=height, color=color))

    def write_string(self, x, y, text):
        # set cursor
        self.write_command("7E060100000000EF")

        # set Text color
        self.write_command("7E0402f800EF")

        # set text size
        self.write_command("7E030302EF")

        def chunkstring(string, length):
            return [string[0+i:length+i] for i in range(0, len(string), length)]

        for i in range(y*2):
            # new line
            self.write_command("7E0210EF")
            self.write_command("7E0210EF")

        text_list = chunkstring(text, 5)
        for _, text in enumerate(text_list):
            text = text_to_hex(text.ljust(5))
            self.write_command("7E0711{text}EF".format(text=text))


class Eye:
    def __init__(self):
        """
        For finding black lines
        """
        # white and black threshold
        #self.white_and_black_threshold = 14
        self.white_and_black_threshold = 40
        # for reducing noises in image
        self.erosion_size = 2
        # for infinite lines
        self.horizontal_angle_range = 30
        self.vertical_angle_range = 30
        self.theta = 0
        """
        For center detection
        """
        # for getting the center area
        self.vertical_center_bar_width = screen_width // 10
        self.vertical_center_bar_top_left = (((screen_width//2)-(self.vertical_center_bar_width//2)), 0)
        self.vertical_center_bar_bottom_right = (((screen_width//2)+(self.vertical_center_bar_width//2)), screen_height)
        self.horizontal_center_bar_width = screen_height // 10
        self.horizontal_center_bar_top_left = (0, ((screen_height//2)-(self.horizontal_center_bar_width//2)))
        self.horizontal_center_bar_bottom_right = (screen_width, ((screen_height//2)+(self.horizontal_center_bar_width//2)))

    def get_center_point_of_a_line(self, line):
        x = (line.x1() + line.x2()) // 2
        y = (line.y1() + line.y2()) // 2
        #print(x, y)
        return x, y

    def is_the_point_at_the_vertical_center_bar_of_the_screen(self, x, y):
        if (x >= self.vertical_center_bar_top_left[0] and x <= self.vertical_center_bar_bottom_right[0]):
            return True
        else:
            return False

    def is_the_point_at_the_horizontal_center_bar_of_the_screen(self, x, y):
        if (y >= self.horizontal_center_bar_top_left[1] and y <= self.horizontal_center_bar_bottom_right[1]):
            #print(self.vertical_center_bar_top_left[0], x, self.vertical_center_bar_bottom_right[0])
            return True
        else:
            return False

    def find_black_lines(self, img, copy=True):
        grayscale_img = img.to_grayscale(copy=copy)
        binary_img = grayscale_img.binary([(0, self.white_and_black_threshold)], invert=True, copy=copy)
        binary_img.erode(self.erosion_size)
        lines = binary_img.find_lines(threshold=9000, theta_margin=25, rho_margin=25)
        result_list = []
        for l in lines:
            # theta_margin: it should change according to the angle-change a drone will make when it's in flying
            # rho_margin: the larger rho is, the thicker the line
            self.theta = l.theta()
            x, y = self.get_center_point_of_a_line(l)
            item = {
                "x0": l.x1(),
                "y0": l.y1(),
                "x1": l.x2(),
                "y1": l.y2(),
                "center_x": x,
                "center_y": y,
                "vertical_center": False,
                "horizontal_center": False,
            }
            if (179-self.vertical_angle_range <= self.theta <= 179) or (0 <= self.theta <= 0+self.vertical_angle_range):
                img.draw_line(l.line(), color=(0, 255, 0))
                item["direction"] = "vertical"
                item["vertical_center"] = self.is_the_point_at_the_vertical_center_bar_of_the_screen(x, y)
                result_list.append(item)
            elif (90-self.horizontal_angle_range <= self.theta <= 90+self.horizontal_angle_range):
                img.draw_line(l.line(), color=(255, 0, 0))
                item["direction"] = "horizontal"
                item["horizontal_center"] = self.is_the_point_at_the_horizontal_center_bar_of_the_screen(x, y)
                result_list.append(item)
        return result_list


class FlyingController:
    def __init__(self):
        pass

    def go_up(self):
        pass

    def go_down(self):
        pass

    def go_straight(self):
        pass

    def go_back(self):
        pass

    def keep_still(self):
        pass

    def stop(self):
        pass


#lcd = SmartOpen_LCD()
#lcd_width = 320
#lcd_height = 240

controller = FlyingController()
eye = Eye()

states = {
    "vertical_line": 0,
}
minimun_duration_for_vertical_line_counting = 4 * 1000
#minimun_duration_for_vertical_line_counting = 10
time_start_for_vertical_line_count = pyb.millis()

while(True):
    img = sensor.snapshot()

    if enable_lens_corr:
        img.lens_corr(1.8)  # for 2.8mm lens...

    #eye.find_black_lines(img, copy=False)
    result_list = eye.find_black_lines(img, copy=True)
    for item in result_list:
        vertical_center = item["vertical_center"]
        horizontal_center = item["horizontal_center"]
        if vertical_center == True and horizontal_center == False:
            duration_since_the_last_detect = pyb.elapsed_millis(time_start_for_vertical_line_count)
            if duration_since_the_last_detect > minimun_duration_for_vertical_line_counting:
                states["vertical_line"] = states["vertical_line"] + 1
                time_start_for_vertical_line_count = pyb.millis()

    print("the number of vertical_center_line we met: ", states["vertical_line"])
