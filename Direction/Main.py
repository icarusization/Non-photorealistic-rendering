# Data: 2016/10/07    Writer: Xu Dewei
# Purpose: It is used to small the size of the sketch line. However there still exist problems since it need you
# judge how many times to iterate and it cann't process the condition when different lines have different widths.
import Image

im=Image.open('retu1.bmp')
(length, width) = im.size

m = {}

def neighbour(point, dic, l_max, w_max):
    x, y = point[0], point[1]
    l = []
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            if 0<=i<l_max and 0<=j<w_max and (i!=x or j!=y):
                if dic.has_key((i, j)):
                    l.append((i, j))
    return l

k1 = range(length+2)
k2 = range(width+2)
k1 = map(lambda x:x-1, [y for y in k1])
k2 = map(lambda x:x-1, [y for y in k2])
for i in k1:
    for j in k2:
        if 0<=i<length and 0<=j<width:
            color = im.getpixel((i, j))
            light = color[0] / 255.0
            if light < 0.5:
                m[(i, j)] = 0
            else:
                m[(i, j)] = 1
        else:
            m[(i, j)] = 0

f = {}
for i in range(length):
    for j in range(width):
        f[(i, j)] = 0
n = 10
for k in range(n):
    for i in range(length):
        for j in range(width):
            num = 0
            for point in neighbour((i, j), m, length, width):
                if m[point]==1:
                    num += 1
            if num>2:
                sum_m = m[(i - 1, j)] + m[(i - 1, j - 1)] + m[(i, j - 1)]
                if sum_m > 1:
                    f[(i, j)] = 1
                else:
                    f[(i, j)] = 0
    for i in range(length):
        for j in range(width):
            if f[(i, j)]==0:
                m[(i, j)] = 0

for i in range(length):
    for j in range(width):
        if f[(i, j)]==1:
            im.putpixel((i, j), (255, 255, 255))
        else:
            im.putpixel((i, j), (0, 0, 0))
im.show()