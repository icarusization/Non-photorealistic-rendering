import random
import Strokes
import math
import Image, ImageDraw
import numpy as np


def neighbour(point, dic, l_max, w_max):
    x, y = point[0], point[1]
    l = []
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            if 0<=i<l_max and 0<=j<w_max and (i!=x or j!=y):
                if dic.has_key((i, j)):
                    l.append((i, j))
    return l


def direction_sketch(im):
    (length, width) = im.size
    m = np.zeros((length, width), np.int)
    for i in range(length):
        for j in range(width):
            color = im.getpixel((i, j))
            light = color[0]/255.0
            if light<0.5:
                m[i][j] = 0
            else:
                m[i][j] = 1

    f = {}
    for i in range(length):
        for j in range(width):
            f[(i, j)] = [0, 0.0]

    angle_dic = {(1, 0):0.0, (1, 1):0.78, (0, 1):1.54, (-1, 1):2.35, (-1, 0):3.14,
                 (-1, -1):3.92, (0, -1):4.71, (1, -1):5.49}
    for i in range(length):
        for j in range(width):
            point = [i, j]
            if m[i][j] ==1:
                l = neighbour(point, f, length, width)
                for p in l:
                    if m[p[0]][p[1]] == 1:
                        angle = angle_dic[(p[0]-i, p[1]-j)]
                        f[(i, j)] = [1, angle]
                        break
    return f


def random_noise(length, width):
    r = {}
    for i in range(length):
        for j in range(width):
            r[(i, j)] = random.random() * 3.14
    return r


def transfer_data(f, r, length, width):
    dic = {}
    for i in range(length):
        for j in range(width):
            l = []
            if f[(i, j)][0] == 1:
                l.append(f[(i, j)][1])
                l.append(float(1.0))
                dic[(i, j)] = l                    # For line point it has weight 1.0
            else:
                l.append(r[(i, j)])
                l.append(float(0.1))
                dic[(i, j)] = l                    # For noise point it has weight 0.0 to be affected by outline
    return dic


def iteration(n, dic, length, width):
    for k in range(n):
        for i in range(length):
            for j in range(width):
                point = dic[(i, j)]
                if point[1] != 1.0:
                    point = square_central(dic, i, j, length, width)
                    # point[1] = 2*point[1]/(1+point[1])
                    dic[(i, j)] = point
    return dic


def square_central(dic, i, j, length, width):
    angle_list = []
    weight_list = []
    angle = 0
    weight = 0

    for m in [i-1, i, i+1]:
        for n in [j-1, j, j+1]:
            if m>=0 and m<length and n>=0 and n<width and (m!=i or n!=j):
                point = dic[(m, n)]
                angle_list.append(point[0])
                weight_list.append(point[1])

    weight_sum = sum(weight_list)
    if weight_sum != 0:
        for i in range(len(angle_list)):
            angle += angle_list[i]*weight_list[i]
        angle = angle / weight_sum                          # Calculate the relative weight for neighbour points

    angle += random.random() * 3.14 / 80                    # Add a noise on angle to avoid parallel

    l = len(weight_list)
    for i in range(l):
        weight += (weight_list[i]/l)
    weight += random.random()*0.06-0.03
    weight = min((max((0, weight)), 1.0))

    return [angle, weight]


def pop_points(dic, point, w):
    if w!=1:
        w -= 1
        x = range(point[0]-w, point[0]+w, 1)
        y = range(point[1]-w, point[1]+w, 1)
    else:
        x = point[0]
        y = point[1]

    for i in x:
        for j in y:
            if (i, j) in dic:
                del dic[(i, j)]
    return dic


def connect_orientation(dic, max_length, w, im):
    (length, width) = im.size
    stroke_list = []
    pix = im.load()

    while len(dic) != 0:
        key_value = dic.popitem()
        begin = key_value[0]
        s_angle = key_value[1][0]

        axis_line = []
        point, l = begin, 0
        con = True
        color = [0, 0, 0]

        while l<max_length and con:
            con = False
            next_point = []
            for ele in neighbour(point, dic, length, width):
                angle = dic[ele][0]
                COS = math.cos(angle-s_angle)
                if abs(COS)>0.707:
                    con = True
                    next_point.append([ele, COS])

            max = -1.0
            for pair in next_point:
                if pair[1]>max:
                    point = pair[0]
                    max = pair[1]
            axis_line.append(point)
            l += 1

        # color = [color[0]/l, color[1]/l, color[2]/l]
        color = [int(random.random() * 255), int(random.random() * 255), int(random.random() * 255)]
        if l > 10:
            stroke_list.append([begin, point, color])

        for points in axis_line:
            dic = pop_points(dic, points, w)

    return stroke_list


def show_stroke(stroke_list, im):
    (length, width) = im.size
    s = Strokes.Stroke()

    # Here you can revise these parameters according to the introduction in the Strokes Class.
    s.distort = 0.2
    s.shake = 0.3
    s.tapering = 0.5
    s.ColorVariability = 0.5
    s.ShadeVariability = 0.5

    draw = ImageDraw.Draw(im)
    for l in stroke_list:
        color = l[2]
        c = Strokes.Color(color[0], color[1], color[2])
        s.color = c
        w = 5

        draw.line(((l[0][0], l[0][1]), (l[1][0], l[1][1])), fill = 255)
        '''
        points = s.draw_strokes(im, l[0][0], l[0][1], l[1][0], l[1][1], w, s.color)

        for i in range(len(points)):
            p = points[i]
            c = p[2]
            nc = c.get_color()
            nc = (int(nc[0] * 255), int(nc[1] * 255), int(nc[2] * 255))
            if 0<=p[0]<length and 0<=p[1]<width:
                im.putpixel((p[0], p[1]), nc)
        '''
    return im
