import random
import BezierLine
import math


# Process: produce a random number between min and max(no requirement for sequence)(int or float)
# Parameter: min, max---the boundary of the targeted number
#            kind---could be "int" or "float", means the kind of the targeted number
# Return: some random number in the region
def random_num(min, max, kind):  # Return a random int or float number
    if kind == "float":
        max += 0.001
    if kind == "int":
        max += 1
    if min > max:
        c = min
        min = max
        max = c
    if kind == "float":
        if min == max:
            return min
        else:
            return random.uniform(min, max)
    if kind == "int":
        min = int(min)
        max = int(max)
        if min == max:
            return min
        else:
            return random.randint(min, max)


# Process: insert distort*10 points. give random position on y with len*distort/4
# Parameter: num---the number of points inserted to calculate the curve(concern distort)
#            y_max---the boundary of each point(concern distort)
#            y_bias_max---the bias of the next point compared with the previous point(concern length and shake)
# Return: axis_line---the calculated axis line of this stroke[[x,y]]
def distort_axis_line(length, distort, shake):  # len is the length, distort should be in 0~1
    num = max(3, (int)(length * distort / 4))
    y_max = max(2, (int)(length * distort / 5))
    y_bias_max = max(1, (int)(length * shake / 10 / 2))

    points = []
    last_y = 0
    for i in range(num + 1):
        x = int(length * i / num)
        y = random_num(int(max(last_y - y_bias_max, -y_max * min(1, abs(i / num - 0.5)))),
                       int(min(last_y + y_bias_max, y_max * min(1, abs(i / num - 0.5)))), "int")
        last_y = y
        points.append((x, y))

    loop = int(max(3, math.log(length / (num + 1), 2) + 1))  # This is to ensure enough points to fill the line.
    b = BezierLine.Bezier2(points, (0, 0, 0), loop)
    b.render()
    axis_line = b.get_points()
    return axis_line


# Process: construct a Bezier line for the boundary
# Parameter: num---the number of points inserted to calculate the width curve(concern length and tapering)
#            width_bias---the bias of the next width compared with the previous one(concerning width and shake)
# Return: r_points---The down and up point of each point on x-axis[[(x, down),(x, up)]]
def broaden_axis_line(axis_line, length, width, tapering, shake):
    points = []
    last_width = width
    num = max(3, int(length * tapering) / 5)
    width_bias = int(width * shake / 3)
    for i in range(num + 1):
        if i == 0 or i == num:
            x = int(length * i / num)
        else:
            x = int(length * i / num) + random_num(int(-length / num / 3), int(length / num / 3), "int")
        y = random_num(int(max(last_width, width + width_bias) - width_bias),
                       int(min(last_width, width + width_bias) - width_bias), "int")
        last_width = y
        if not (x, y) in points: points.append((x, y))

    loop = int(max(4, math.log(length / (num + 1), 2) + 1))
    b = BezierLine.Bezier2(points, (0, 0, 0), loop)
    b.render()
    width_line = b.get_points()

    r_points = []
    x = -1
    r = 0
    for i in range(len(width_line)):
        while not width_line[i][0] == axis_line[r][0]: r = r + 1
        up = (int)(width_line[i][1] / 2 + 1)
        down = (int)((width_line[i][1] + 1) / 2 - 1)
        x_points = []
        if not width_line[i][0] == x:
            x += 1
            x_points.append((x, -down + axis_line[r][1]))
            x_points.append((x, up + axis_line[r][1]))
            r_points.append(x_points)

    return r_points


# Process: Soften the boundary on the two sides and complete the two side-circle for these points.
# Parameter: points---The data format: For down and up points for each point on x-axis.
#            width---the width of the stroke(we assume the left or right won't pass width/2)
# Return: points---From x from begin-width/2 to end+width/2, with format [[(x, down), (x, up)]]
def soften_points(points, width, shake):
    b = max(2, (int)(width * shake))
    # For left part
    boundary = [(points[0][0][0], points[0][0][1]), (points[0][0][0] - b, -b / 2),
                (points[0][1][0] - b, +b), (points[0][1][0], points[0][1][1])]
    loop = (int)(max(4, math.log(2 * width / 3, 2) + 1))
    left = BezierLine.Bezier2(boundary, (0, 0, 0), loop)
    left.render()
    boundary_line = left.get_points()
    begin = 0
    end = len(boundary_line) - 1
    while begin <= end:
        if boundary_line[begin][0] == boundary_line[end][0]:
            down = 500
            up = -500
            x = boundary_line[begin][0]
            while boundary_line[begin][0] == boundary_line[end][0] == x:
                down = min(down, boundary_line[begin][1])
                up = max(up, boundary_line[end][1])
                begin += 1
                end -= 1
            points.insert(0, [(x, down), (x, up)])
        else:
            if (boundary_line[begin][0] < boundary_line[end][0]):
                end -= 1
            else:
                begin += 1
    # For right part
    boundary = []
    boundary_line = []
    l = len(points) - 1
    boundary = [(points[l][0][0], points[l][0][1]), (points[l][0][0] + b, - b / 2),
                (points[l][1][0] + b, + b), (points[l][1][0], points[l][1][1])]
    right = BezierLine.Bezier2(boundary, (0, 0, 0), loop)
    right.render()
    boundary_line = right.get_points()
    begin = 0
    end = len(boundary_line) - 1
    l = len(points)
    while begin <= end:
        if boundary_line[begin][0] == boundary_line[end][0]:
            down = 500
            up = -500
            x = boundary_line[begin][0]
            while boundary_line[begin][0] == boundary_line[end][0] == x:
                down = min(down, boundary_line[begin][1])
                up = max(up, boundary_line[end][1])
                begin += 1
                end -= 1
            points.insert(l, [(x, down), (x, up)])
            l += 1
        else:
            if (boundary_line[begin][0] > boundary_line[end][0]):
                end -= 1
            else:
                begin += 1

    return points


# Process: Resize these points with experimental length and width with actual length and width
# parameter: points---The full points with experimental length and width
#            lm,wm---the changed size times of length and width
# Return: l---the points with self size(length and width), with format [[(x, down), (x, up)]]
# Attach: In the Strokes we set experimental length = 200 and width = 30 which is flexible
def resize_full_points(points, lm, wm):
    l = []
    b = []
    for i in range(len(points)):
        bi = []
        a = int(points[i][0][0]/lm)
        b = int(points[i][0][1]/wm)
        x = (a, b)
        bi.append(x)
        a = int(points[i][1][0]/lm)
        b = int(points[i][1][1]/wm)
        x = (a, b)
        bi.append(x)
        if not bi in l:
            l.append(bi)
    return l


# Process: describe the important boundary points for insertion calculation in up and down level.
# Parameter: length, width, color --- about the rectangle
# Return: list A of up points + list B of down points
# Attach: Need to begin from -width since the stroke starts there and end with length+width/2
#         The color attribution: mid have biggest s which decrease to two side. Points have the same y share the common
#         v, which varies as x changes.
def color_rectangle(np, color, cv, sv):
    up = []
    down = []
    mid = []
    for i in range(int(np)+2):
        c_v = random_num(min(1.0, color.V * (1 + sv / 6.0)), max(0.0, color.V * (1 - sv / 6.0)), "float")

        c_h = random_num(color.H * (1.0 + cv / 3.0), color.H * (1 - cv / 3.0), "int") % 360
        c_s = random_num(min(1.0, color.S * 1.0), max(0.0, color.S * (1.0 - cv / 2.0)), "float")
        c = (c_h, c_s, c_v)
        up.append(c)

        c_h = random_num(color.H * (1 + cv / 3.0), color.H * (1 - cv / 3.0), "int") % 360
        c_s = random_num(min(1.0, color.S * (1.0 + cv / 8.0)), max(0.0, color.S * (1 - cv / 8.0)), "float")
        c = (c_h, c_s, c_v)
        mid.append(c)

        c_h = random_num(color.H * (1.0 + cv / 3.0), color.H * (1 - cv / 3.0), "int") % 360
        c_s = random_num(min(1.0, color.S * 1.0), max(0.0, color.S * (1.0 - cv / 2.0)), "float")
        c = (c_h, c_s, c_v)
        down.append(c)
    all_color = [up, mid, down]
    return all_color
