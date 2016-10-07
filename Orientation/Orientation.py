import Image
import Implement_For_Orientation as Ip
# Data: 16/09/21       Writer: Xu De Wei
# Give: Orientation field dictionary f,  random noise field dictionary r
# Data format: f[(i, j)]: [0/1, angle]        r[(i, j)]: angle
# Data format: dic[(i, j)]: [angle, weight]

class Orientation:
	def __init__(self):
		self.image=None
		self.iteration_number=None
		self.diffusion_result=None
                self.effect=None

	def set_image(self,im):
		self.image=Image.open('redu.bmp')
		
        
	def set_iternum(self,num):
		self.iternation_number=num

	def Diffusion(self):
		(length, width) = self.image.size
		f = Ip.direction_sketch(im)                       # f is the sketch line graph whose format is f[(i, j)]: [0/1, angle]
		r = Ip.random_noise(length, width)               # produce the graph random noise
		dic = Ip.transfer_data(f, r, length, width)      # input f, r to get the whole graph orientation field
		eff = {}
		eff = Ip.effect_map(dic, length, width)
		dic, eff = Ip.iteration(num, dic, eff, length, width)
		self.dic=dic
		self.eff=eff
		
'''			
im=Image.open('redu.bmp')
(length, width) = im.size

f = Ip.direction_sketch(im)                       # f is the sketch line graph whose format is f[(i, j)]: [0/1, angle]

r = Ip.random_noise(length, width)               # produce the graph random noise

dic = Ip.transfer_data(f, r, length, width)      # input f, r to get the whole graph orientation field
eff = {}

num = 50                                        # iteration times
eff = Ip.effect_map(dic, length, width)
dic, eff = Ip.iteration(num, dic, eff, length, width)

max_length, w = 8, 2                           # the maximum length and width of stroke
stroke_list = Ip.connect_orientation(dic, eff, max_length, w, im)

new_image = Image.new("RGB", (length, width), (255, 255, 255))
new_image = Ip.show_stroke(stroke_list, new_image)

new_image.show()
'''
