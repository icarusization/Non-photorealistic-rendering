import Image, ImageDraw
import Implement as Ip
import random
import math
import vector as vc

# Give: Orientation field dictionary f,  random noise field dictionary r
# Data format: f[(i, j)]: [0/1, angle]        r[(i, j)]: angle
#              dic[(i, j)]: [angle, weight]

im=Image.open('boundary.jpg')
length = 612
width = 496
im1 = Image.new("RGB", (length, width), (255, 255, 255))
im2 = Image.new("RGB", (length*2+1, width*2+1), (255, 255, 255))
f = {}
r = {}

f = vc.direction_array(im)

for i in range(length):
    for j in range(width):
        r[(i, j)] = random.random()*3.14

dic = {}

# First read the data from f, r into dic
dic = Ip.transfer_data(f, r, dic)

# Get into iterations to converge direction b
n = 30    # iteration times
dic = Ip.iteration(n, dic)

draw = ImageDraw.Draw(im2)
for i in range(length-1):
    for j in range(width-1):
        h = dic[(i, j)][0]
        r, g, b = Ip.hsv2rgb(h/6.28*360, 1.0, 1.0)
        im1.putpixel((i, j), (r, g, b))
        newi = int(i*10+5+10.0*math.cos(h))
        newj = int(j*10+5+10.0*math.sin(h))
        draw.line(((i*10+5, j*10+5),(newi, newj)),fill=128)
        if 1 < newi < length-1 and 1 < newj < width-1:
            if newi > i * 10 + 5:
                im2.putpixel((newi - 1, newj), (0, 0, 0))
            else:
                im2.putpixel((newi + 1, newj), (0, 0, 0))
            if newj > j * 10 + 5:
                im2.putpixel((newi, newj - 1), (0, 0, 0))
            else:
                im2.putpixel((newi, newj + 1), (0, 0, 0))

im1.show()
im2.show()

pass



