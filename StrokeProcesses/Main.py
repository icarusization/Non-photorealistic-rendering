import Image
import Implement_For_Orientation as Ip
# Data: 16/09/21       Writer: Xu De Wei
# Give: Orientation field dictionary f,  random noise field dictionary r
# Data format: f[(i, j)]: [0/1, angle]        r[(i, j)]: angle
# Data format: dic[(i, j)]: [angle, weight]
orim = Image.open('mixcolor.jpg')
im=Image.open('retu1.bmp')
(length, width) = im.size

f = Ip.direction_sketch(im)                       # f is the sketch line graph whose format is f[(i, j)]: [0/1, angle]

r = Ip.random_noise(length, width)               # produce the graph random noise

dic = Ip.transfer_data(f, r, length, width)      # input f, r to get the whole graph orientation field
eff = {}

num = 50                                        # iteration times
eff = Ip.effect_map(dic, length, width)
dic, eff = Ip.iteration(num, dic, eff, length, width)

#samplelist
#orientationlist
#sizelist
#colorlist
'''
max_length, w = 15, 2                           # the maximum length and width of stroke e.g(15,4)
stroke_list = Ip.connect_orientation(dic, eff, max_length, w, im, orim)
'''
#construct the stroke list
#[[(x1,y1),[x2,y2],rgb],...]
new_image = Image.new("RGB", (length, width), (255, 255, 255))
new_image = Ip.show_stroke(stroke_list, new_image)

new_image.show()
