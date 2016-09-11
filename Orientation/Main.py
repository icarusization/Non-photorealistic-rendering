import Image
import Implement as Ip
import random

# Give: Orientation field dictionary f,  random noise field dictionary r
# Data format: f[(i, j)]: [0/1, angle]        r[(i, j)]: angle
#              dic[(i, j)]: [angle, weight]

length = 100
width = 100
im = Image.new("RGB", (length, width), (255, 255, 255))
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
        f[(i, j)] = [1, 1.53]

newrange2 = range(50)
for i in newrange2:
    newrange2[i] += 22
for i in newrange2:
    for j in [63]:
        f[(i, j)] = [1, 2.09]

f[(10, 8)] = [1, 1.53]
f[(10, 9)] = [1, 1.52]
f[(10, 10)] = [1, 1.51]
f[(10, 11)] = [1, 1.50]
f[(10, 12)] = [1, 1.51]


dic = {}

# First read the data from f, r into dic
dic = Ip.transfer_data(f, r, dic)

# Get into iterations to converge direction
n = 50     # iteration times
dic = Ip.iteration(n, dic)

for i in range(length):
    for j in range(width):
        k = dic[(i, j)][0]/3.14
        color = 255-int(255*k)
        im.putpixel((i, j), (color, color, color))

im.show()

pass



