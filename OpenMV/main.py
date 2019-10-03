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
#sensor.set_pixformat(sensor.GRAYSCALE)  # grayscale is faster
sensor.set_framesize(sensor.QQVGA)  # QVGA: 320x240, QQVGA: 160x120
sensor.skip_frames(time=2000)

enable_lens_corr = True  # turn on for straighter lines...

# white and black threshold
THRESHOLD = 14

# for getting screen resolution
screen_width = sensor.width()
screen_height = sensor.height()

# for line segments
line_segment_merging_distance = screen_width // 8
max_theta_difference = 15
# take 3 points at that line, if at least 2 point is black, we say it's a black line

# for infinite lines
horizontal_range = 30
vertial_range = 30
theta = 0
# take 3 points at that line, if at least 1 point is black, we say it's a black line

def is_a_black_line(line, img):
    x1, y1, x2, y2 = line.line()
    point1 = (int((1/4)*x2 + (3/4)*x1), int((1/4)*y2 + (3/4)*y1))
    point2 = (int((2/4)*x2 + (2/4)*x1), int((2/4)*y2 + (2/4)*y1))
    point3 = (int((3/4)*x2 + (1/4)*x1), int((3/4)*y2 + (1/4)*y1))
    points = [point1, point2, point3]

    total_points = len(points)
    black_points = 0
    for x,y in points:
        value = img.get_pixel(x, y)
        if (value != None):
            value = image.rgb_to_grayscale(value)
            if (value <= THRESHOLD):
                black_points += 1

    if black_points / total_points > 0.6:
    #if black_points > 0:
        return True
    else:
        return False

def find_lines(img):
    for l in img.find_line_segments(merge_distance=line_segment_merging_distance, max_theta_diff=5):
    #for l in img.find_lines(threshold=7000, theta_margin=25, rho_margin=25):
        if (is_a_black_line(l, img)):
            theta = l.theta()
            if (179-horizontal_range <= theta <= 179) or (0 <= theta <= 0+horizontal_range):
                img.draw_line(l.line(), color=(0, 255, 0))
            elif (90-vertial_range <= theta <= 90+vertial_range):
                img.draw_line(l.line(), color=(255, 0, 0))

        """
        the parent_line object:
        {"x1":226, "y1":0, "x2":226, "y2":239, "length":239, "magnitude":8778, "theta":0, "rho":226}

        the method of that parent_line:
        ['line', 'x1', 'y1', 'x2', 'y2', 'length', 'magnitude', 'theta', 'rho']
        > use it by calling it, like line.length()

        the parent_line object:
        (202, 0, 194, 239)

        the range of theta is (0, 179)
        """

while(True):
    img = sensor.snapshot()

    if enable_lens_corr:
        img.lens_corr(1.8)  # for 2.8mm lens...

    find_lines(img)
