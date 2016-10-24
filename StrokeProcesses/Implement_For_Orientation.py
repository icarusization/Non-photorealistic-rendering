import random
import Strokes
import numpy as np

if_dic = {}
for i in range(197):
    for j in range(189):
        if_dic[(i, j)] = 0


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
    length, width,_ = im.shape
    m = np.zeros((length, width), np.int)
    for i in range(length):
        for j in range(width):
            color = im[i,j]
            light = color[0]/255.0
            if light < 0.5:
                m[i][j] = 0
            else:
                m[i][j] = 1

    f = {}
    for i in range(length):
        for j in range(width):
            f[(i, j)] = [0, 0.0]

    angle_dic = {(1, 0): 0.0, (1, 1): 0.78, (0, 1): 1.54, (-1, 1): 2.35, (-1, 0): 3.14,
                 (-1, -1): 3.92, (0, -1): 4.71, (1, -1): 5.49}
    for i in range(length):
        for j in range(width):
            point = [i, j]
            if m[i][j] == 1:
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
            r[(i, j)] = random.random() * 6.28
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


def effect_map(dic, length, width):
    eff = {}
    for i in range(length):
        for j in range(width):
            if dic[(i, j)][1] == 1.0:
                eff[(i, j)] = 1.0
            else:
                eff[(i, j)] = 0.0
    return eff


def iteration(n, dic, eff, length, width):
    new_eff = eff.copy()

    for k in range(n):
        for i in range(length):
            for j in range(width):
                point = dic[(i, j)]
                cp = [i, j]
                '''

                if point[1] != 1.0:
                    point = square_central(dic, i, j, length, width)
                    dic[(i, j)] = point


                ave, var = float(0), float(0)
                neigh_point = neighbour(cp, dic, length, width)
                for p in neigh_point:
                    ave += eff[p]
                ave /= len(neigh_point)
                for p in neigh_point:
                    var += (eff[p]-ave)**2
                var = math.sqrt(var/len(neigh_point))
                if var>0.0001:
                    for p in neigh_point:
                        new_eff[(i, j)] += eff[p]
                    if k % 5 == 0:
                        new_eff[(i, j)] *= (1 + random.random() * 0.5)
                    new_eff[(i, j)] = new_eff[(i, j)] / 9
                '''
                neigh_point = neighbour(cp, dic, length, width)
                for p in neigh_point:
                    new_eff[(i, j)] += eff[p]

                if k % 5 == 0:
                    new_eff[(i, j)] *= 1 # (1+random.random()*0.5)
                new_eff[(i, j)] = new_eff[(i, j)] / (len(neigh_point)+1)

        eff = new_eff.copy()
    return dic, eff


def square_central(dic, i, j, length, width):
    angle_list = []
    weight_list = []
    angle = 0
    weight = 0

    for m in [i-1, i, i+1]:
        for n in [j-1, j, j+1]:
            if 0 <= m < length and 0 <= n < width and (m != i or n != j):
                point = dic[(m, n)]
                angle_list.append(point[0])
                weight_list.append(point[1])

    weight_sum = sum(weight_list)

    if weight_sum != 0:
        cp = dic[(i, j)]
        for i in range(len(angle_list)):
            angle += angle_list[i]*weight_list[i]

        # angle  = angle/weight_sum
        angle = cp[0]*cp[1]+(1-cp[1])*angle / weight_sum

    angle += random.random() * 3.14 / 80                    # Add a noise on angle to avoid parallel

    l = len(weight_list)
    for i in range(l):
        weight += (weight_list[i] / l)
    weight += random.random() * 0.03 - 0.015
    weight = min((max((0, weight)), 1.0))
    '''
    angle = dic[(i, j)][0]
    weight = dic[(i, j)][1]
    if weight_sum != 0 and if_dic[(i, j)]==0:
        k = 0
        for i in range(len(angle_list)):
            if weight_list[i] == 1.0:
                angle += angle_list[i]
                k += 1
        if k!=0:
            angle = angle/k
            weight = 1.0
            if_dic[(i, j)] = 1
    '''
    return [angle, weight]


def pop_points(dic, point, w):
    if w!=1:
        w -= 1
        x = range(point[0]-w, point[0]+w, 1)
        y = range(point[1]-w, point[1]+w, 1)
    else:
        x = [point[0]]
        y = [point[1]]

    for i in x:
        for j in y:
            if (i, j) in dic:
                del dic[(i, j)]
    return dic

def get_origin_color(orim, axis_line):
    r, g, b = 0, 0, 0
    for points in axis_line:
        the_color = orim.getpixel(points)
        r += the_color[0]
        g += the_color[1]
        b += the_color[2]
    le = len(axis_line)
    if le != 0:
        r /= le
        g /= le
        b /= le
    return [r, g, b]

def connect_orientation(dic, eff, max_length, w, im, orim):
    (length, width) = im.size
    stroke_list = []

    while len(dic) != 0:
        #iterate list
        key_value = dic.popitem()
        begin = key_value[0]
        s_angle = key_value[1][0]

        s_weight = key_value[1][1]

        axis_line = []
        point, l = begin, 0
        con = True
        color = [0, 0, 0]

        while l<max_length and con:

            con = False
            next_point = []
            '''
            # Arrange by weight
            for ele in neighbour(point, dic, length, width):
                weight = dic[ele][1]
                wd = abs(weight - s_weight)
                if abs(wd) < 0.1:
                    con = True
                    next_point.append([ele, wd])

            min = 1.0
            for pair in next_point:
                if pair[1] < min:
                    point = pair[0]
                    min = pair[1]

            axis_line.append(point)
            l += 1
            '''
            s_effect = eff[point]
            for ele in neighbour(point, dic, length, width):
                effect = eff[ele]
                ed = abs(effect-s_effect)
                if abs(ed) < 0.5:
                    con = True
                    next_point.append([ele, ed])

            min = 100
            for pair in next_point:
                if pair[1] < min:
                    point = pair[0]
                    min = pair[1]

            dic = pop_points(dic, point, w)
            axis_line.append(point)
            l += 1

        color = get_origin_color(orim, axis_line)
        # color = [int(random.random() * 255), int(random.random() * 255), int(random.random() * 255)]

        if l > 5:
            stroke_list.append([begin, point, color])
        '''
        for points in axis_line:
            dic = pop_points(dic, points, w)
        '''

    return stroke_list

'''
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

        points = s.draw_strokes(im, l[0][0], l[0][1], l[1][0], l[1][1], w, s.color)

        for i in range(len(points)):
            p = points[i]
            c = p[2]
            nc = c.get_color()
            nc = (int(nc[0] * 255), int(nc[1] * 255), int(nc[2] * 255))
            if 0<=p[0]<length and 0<=p[1]<width:
                im.putpixel((p[0], p[1]), nc)

    return im
'''
