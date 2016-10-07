# Data: 2016/10/07    Writer: Xu Dewei
# Purpose: It is used to divide the picture into 10*10 squares to fit the function so that we can get the angle by
# calculating the derivatives.
import Image

im=Image.open('retu1.bmp')
(length, width) = im.size

m = {}
for i in range(length):
    for j in range(width):
        if 0<=i<length and 0<=j<width:
            color = im.getpixel((i, j))
            light = color[0] / 255.0
            if light < 0.5:
                m[(i, j)] = 0
            else:
                m[(i, j)] = 1
        else:
            m[(i, j)] = 0

il = length/10-1
jl = width/10-1
angle = {}
for i in range(il):
    for j in range(jl):
        ilist = map(lambda x: x+il*10, [y for y in range(10)])
        jlist = map(lambda x: x+jl*10, [y for y in range(10)])
        hlist = []
        for x in ilist:
            sum, num = 0, 0
            for y in jlist:
                if m[(x, y)]==1:
                    sum += y
                    num += 1
            if num!=0:
                sum /= num
            hlist.append(sum)
        # angle_list = Func(ilist, hlist)
        angle_list = range(10)

        for x in ilist:
            num = 0
            for y in jlist:
                if m[(x, y)]==1:
                    angle[(x, y)] = angle_list[num]
            num += 1
