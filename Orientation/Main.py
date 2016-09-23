import Image
import Implement as Ip
import vector as vc
# Data: 16/09/21       Writer: Xu De Wei
# Give: Orientation field dictionary f,  random noise field dictionary r
# Data format: f[(i, j)]: [0/1, angle]        r[(i, j)]: angle
# Data format: dic[(i, j)]: [angle, weight]

im=Image.open('retu1.bmp')
(length, width) = im.size

f = Ip.direction_sketch(im)                       # f is the sketch line graph whose format is f[(i, j)]: [0/1, angle]

r = Ip.random_noise(length, width)               # produce the graph random noise

dic = Ip.transfer_data(f, r, length, width)      # input f, r to get the whole graph orientation field

num = 30                                       # iteration times
dic = Ip.iteration(num, dic, length, width)

max_length, w = 20, 3                            # the maximum length and width of stroke
stroke_list = Ip.connect_orientation(dic, max_length, w, im)

new_image = Image.new("RGB", (length, width), (255, 255, 255))
new_image = Ip.show_stroke(stroke_list, new_image)

new_image.show()
