import Image, ImageDraw
import Implement as Ip
import random
import math

# Give: Orientation field dictionary f,  random noise field dictionary r
# Data format: f[(i, j)]: [0/1, angle]        r[(i, j)]: angle
#              dic[(i, j)]: [angle, weight]

length = 100
width = 100
im = Image.new("RGB", (length, width), (255, 255, 255))
im2 = Image.new("RGB", (length*10+1, width*10+1), (255, 255, 255))
f = {}
r = {}

for i in range(length):
    for j in range(width):
        f[(i, j)] = [0, float(0.0)]
        r[(i, j)] = random.random()*3.14

newrange = range(35)
for i in newrange:
    newrange[i] += 34
for i in newrange:
    for j in [47]:
        f[(i, j)] = [1, 1.23]

newrange2 = range(50)
for i in newrange2:
    newrange2[i] += 22
for i in newrange2:
    for j in [63]:
        f[(i, j)] = [1, -2.89]

f[(10, 8)] = [1, 1.53]
f[(10, 9)] = [1, 1.52]
f[(10, 10)] = [1, 1.51]
f[(10, 11)] = [1, 1.50]
f[(10, 12)] = [1, 1.51]


dic = {}

# First read the data from f, r into dic
dic = Ip.transfer_data(f, r, dic)

# Get into iterations to converge direction
n = 100    # iteration times
dic = Ip.iteration(n, dic)

draw = ImageDraw.Draw(im2)
for i in range(length-1):
    for j in range(width-1):
        h = dic[(i, j)][0]/3.14
        r, g, b = Ip.hsv2rgb(h*360, 1.0, 1.0)
        im.putpixel((i, j), (r, g, b))
        newi = int(i*10+5+10.0*math.cos(h))
        newj = int(j*10+5+10.0*math.sin(h))
        draw.line(((i*10+5, j*10+5),(newi, newj)),fill=128)
        if newi>i*10+5:
            im2.putpixel((newi-1, newj),(0, 0, 0))
        else:
            im2.putpixel((newi+1, newj),(0, 0, 0))
        if newj > j * 10 + 5:
            im2.putpixel((newi, newj-1), (0, 0, 0))
        else:
            im2.putpixel((newi, newj+1), (0, 0, 0))

im.show()
im2.show()

pass



