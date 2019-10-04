# find_black_lines - By: yingshaoxo - Wed Oct 2 2019

# 注意：线条检测是通过使用霍夫变换完成的：
# http://en.wikipedia.org/wiki/Hough_transform
# 请阅读以上关于“theta”和“rho”的更多信息。

# find_lines（）找到无限长度的线。使用find_line_segments（）
# 来查找非无限线。

import time
import image
import sensor

sensor.reset()
sensor.set_pixformat(sensor.RGB565)  # grayscale is faster
# sensor.set_pixformat(sensor.GRAYSCALE)  # grayscale is faster
sensor.set_framesize(sensor.QQVGA)  # QVGA: 320x240, QQVGA: 160x120
sensor.skip_frames(time=2000)

enable_lens_corr = True  # turn on for straighter lines...

# for getting screen resolution
screen_width = sensor.width()
screen_height = sensor.height()


class Eye:
    def __init__(self):
        """
        For finding black lines
        """
        # white and black threshold
        self.white_and_black_threshold = 14
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
        self.vertical_center_bar_width = screen_width // 8
        self.vertical_center_bar_top_left = (((screen_width//2)-(self.vertical_center_bar_width//2)), 0)
        self.vertical_center_bar_bottom_right = (((screen_width//2)+(self.vertical_center_bar_width//2)), screen_height)
        self.horizontal_center_bar_width = screen_height // 8
        self.horizontal_center_bar_top_left = (0, ((screen_height//2)-(self.horizontal_center_bar_width//2)))
        self.horizontal_center_bar_bottom_right = (screen_width, ((screen_height//2)+(self.horizontal_center_bar_width//2)))

    def get_center_point_of_a_line(self, line):
        x = (line.x1() + line.x2()) // 2
        y = (line.y1() + line.y2()) // 2
        print(x, y)
        return x, y

    def is_the_point_at_the_vertical_center_bar_of_the_screen(self, x, y):
        if (x >= self.vertical_center_bar_top_left[0] and x <= self.vertical_center_bar_bottom_right[0]):
            return True
        else:
            return False

    def is_the_point_at_the_horizontal_center_bar_of_the_screen(self, x, y):
        if (y >= self.horizontal_center_bar_top_left[1] and y <= self.horizontal_center_bar_bottom_right[1]):
            print(self.vertical_center_bar_top_left[0], x, self.vertical_center_bar_bottom_right[0])
            return True
        else:
            return False

    def find_black_lines(self, img):
        grayscale_img = img.to_grayscale(copy=True)
        binary_img = grayscale_img.binary([(0, self.white_and_black_threshold)], invert=True, copy=True)
        binary_img.erode(self.erosion_size)
        lines = binary_img.find_lines(threshold=9000, theta_margin=25, rho_margin=25)
        for l in lines:
            # theta_margin: it should change according to the angle-change a drone will make when it's in flying
            # rho_margin: the larger rho is, the thicker the line
            self.theta = l.theta()
            x, y = self.get_center_point_of_a_line(l)
            if (179-self.vertical_angle_range <= self.theta <= 179) or (0 <= self.theta <= 0+self.vertical_angle_range):
                img.draw_line(l.line(), color=(0, 255, 0))
            elif (90-self.horizontal_angle_range <= self.theta <= 90+self.horizontal_angle_range):
                img.draw_line(l.line(), color=(255, 0, 0))


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


controller = FlyingController()
eye = Eye()
while(True):
    img = sensor.snapshot()

    if enable_lens_corr:
        img.lens_corr(1.8)  # for 2.8mm lens...

    eye.find_black_lines(img)
