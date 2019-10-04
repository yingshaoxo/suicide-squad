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

# white and black threshold
THRESHOLD = 14

# for reducing noises in image
EROSION_SIZE = 2

# for infinite lines
horizontal_range = 30
vertical_range = 30
theta = 0


def find_lines(img):
    grayscale_img = img.to_grayscale(copy=True)
    binary_img = grayscale_img.binary([(0, THRESHOLD)], invert=True, copy=True)
    binary_img.erode(EROSION_SIZE)
    for l in binary_img.find_lines(threshold=9000, theta_margin=25, rho_margin=25):
        # theta_margin: it should change according to the angle-change a drone will make when it's in flying
        # rho_margin: the larger rho is, the thicker the line
        theta = l.theta()
        if (179-vertical_range <= theta <= 179) or (0 <= theta <= 0+vertical_range):
            img.draw_line(l.line(), color=(0, 255, 0))
        elif (90-horizontal_range <= theta <= 90+horizontal_range):
            img.draw_line(l.line(), color=(255, 0, 0))


while(True):
    img = sensor.snapshot()

    if enable_lens_corr:
        img.lens_corr(1.8)  # for 2.8mm lens...

    find_lines(img)
