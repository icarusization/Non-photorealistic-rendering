import math
import random
import matplotlib.pyplot as plt
from curve_final_dict import Single_curve as Sc

import Image

#Input:
#	One 2-dimension lists contains edges of a segment. Edge pixels are 'True' while others are 'False';
#	a list of color(rgb).
#
#Output:
#	To the curve: 
#		two 2/-dimension lists contain the upper and lower lines of a curve. ?The position is the relative position? ;
#		a list of color(rgb).
#	To the layer: a 2-dimension lists of image of the segment.
#
#Others:
#	Segment_edges, image, line_b, and line_d are all 2-dimension lists.
#	Vertical is x, Horizontal is y

class Seg_layer:
	def __init__(self,edges,pix,canvas,im):
		self.pix = pix #pix dict from segment {(x,y):(r,g,b)}
		self.edges=edges # sorted edges list from segment (x,y)
		#self.render_type = 0 #render type
		self.alpha = 0.2 #angle between line and horizontal axis, range in 0 to pi/2
		self.bs = 8 #brush size	
		self.plo = 2 #parallel line overlap
		self.wd = 30 #wobble distance
		self.wr = 1 #wobble radius
		self.cov = 70 #coverage of the segment
		self.bd = 1 #boundary decrease
		self.bds = 1 #decrease steps
		self.bm = 1 #boundary movement
		self.line_top_l = [] #points of line about the upper bound of the curve (x,y)
		self.line_bottom_l = [] #points of line about the lower bound of the curve (x,y)
		self.line_top = {} #corresponding dict
		self.line_bottom = {} #corresponding dict
		self.line_pix = {} #pixels of curve {(x,y):(r,g,b)}
		self.canvas = canvas
		self.im=im
		#self.sc = Sc(self.line_top,self.line_bottom,1,self.canvas,fig1,self.im)
		

	def render(self,render_type=0):
		if render_type == 0:
			self.parallel()

	def parallel(self):
		min_edge_x = min(self.edges)[0]-5
		max_edge_x = max(self.edges)[0]+5
		min_edge_y = 10000
		max_edge_y = 0
		for i in range(len(self.edges)):
			if min_edge_y > self.edges[i][1]:
				min_edge_y = self.edges[i][1]
			if max_edge_y < self.edges[i][1]:
				max_edge_y = self.edges[i][1]
		min_edge_y = min_edge_y-5
		max_edge_y = max_edge_y+5
		interval = int(abs((self.bs-self.plo)/math.cos(self.alpha)))
		#print "max_x=",max_edge_x," min_x=",min_edge_x,"max_y=",max_edge_y," min_y=",min_edge_y
		start = (0,0)
		end = (0,0)
		count = 0
		if self.alpha == math.pi/2:
			self.alpha = math.pi/2-0.01
		if self.alpha == 0:
			self.alpha = 0.01
		min_x = 0
		if self.alpha < math.pi/2:
			min_x = int(min_edge_x - (max_edge_y-min_edge_y)*math.tan(self.alpha))
			max_x = max_edge_x
		else:
			min_x = min_edge_x
			max_x = int(max_edge_x - (max_edge_y-min_edge_y)*math.tan(self.alpha))
		#max_x = int(max_edge_x + (max_edge_y-min_edge_y)*math.tan(self.alpha))
		#print "min=",min_x," max=",max_x
		get_start = False
		step = 0
		cur_x = 0
		cur_y = 0
		cur_in_check = False
		#Suppose edges are sorted
		while (min_x+interval*count <= max_x):
			if self.alpha >= math.pi*3/4 and self.alpha < math.pi:
				cur_x = int(min_x+interval*count+step*math.tan(self.alpha))
				cur_y = int(min_edge_y+step)
			elif self.alpha > math.pi/2: 
				cur_x = int(min_x+interval*count-step)
				cur_y = int(min_edge_y-step/math.tan(self.alpha))
			elif self.alpha > math.pi/4:
				cur_x = int(min_x+interval*count+step)
				cur_y = int(min_edge_y+step/math.tan(self.alpha))
				#print cur_x,cur_y,math.tan(self.alpha)
			elif self.alpha > 0:
				cur_x = int(min_x+interval*count+step*math.tan(self.alpha))
				cur_y = int(min_edge_y+step)
			else:
				print "Error!"
			if (self.alpha < math.pi/2 and (cur_x > max_edge_x or cur_y > max_edge_y)) or (self.alpha > math.pi/2 and (cur_x < min_edge_x or cur_y > max_edge_y)):
				count = count + 1
				step = 0
				get_start = False
				continue
			if (cur_x,cur_y) in self.edges:
				cur_in_check = True
			else:
				if cur_in_check == True:
					#print count," ",cur_x," ",cur_y
					if get_start == True:
						end = (cur_x,cur_y)
						#if self.edges[i][0] == start[0]:
						#	end = self.edges[i]
						point_list = self.get_point(start,end)
						#print point_list
						for j in range(len(point_list)-1):
							self.line_top_l = []
							self.line_bottom_l = []
							self.line_top = {}
							self.line_bottom = {}
							self.line_pix = {}
							self.draw_curve(point_list[j],point_list[j+1])
						get_start = False
						#if i < len(self.edges)-1 and self.edges[i+1][0] > self.edges[i][0]:
						#	count = count + 1
						#else:
						#	print "edges have error at x=",self.edges[i][0]
					else:					
						#if self.edges[i][0] >= min_edge_x+interval*count:
						#	if i == len(self.edges)-1 or self.edges[i+1][0] != self.edges[i][0]:
						#		continue
						start = (cur_x,cur_y)
						get_start = True
				cur_in_check = False
			step = step + 1
				
	def draw_curve(self,s,e):
                #fig1 = plt.figure()
		fig1=None
		line = self.brush(s,e)
		self.get_line_tb(line)
		self.get_line_pix()
		sc = Sc(self.line_top, self.line_bottom, 1 , self.canvas, fig1 ,self.im)
		sc.render()
		
		#for (key,value) in self.line_top.items():
		#	plt.scatter(key[0],key[1])
		#for (key,value) in self.line_pix.items():
		#	plt.scatter(key[0],key[1])
		'''print "Start_point: ",s
		print "End_point: ",e
		print "Line_top (list): ",self.line_top
		print "Line_bottom (list): ",self.line_bottom
		#print "Line_pix (dict): ",self.line_pix
		print "--------------------------------------------------------------------"
		'''

	def adjust_point(self,p):
		theta=random.uniform(0,2*math.pi)
		p=(int(p[0]+round(self.wr*math.cos(theta))),int(p[1]+round(self.wr*math.sin(theta)))) #move point randomly in a circle of radius wr
		return p

	def get_line_pix(self): #list devided into stroke
		up = []
		down = []
		max_constant = 10000
		min_y = max_constant
		max_y = 0
		for i in range(len(self.line_top_l)): #Find min_y and max_y of line
			if self.line_top_l[i][1] < min_y: min_y = self.line_top_l[i][1]
			if self.line_top_l[i][1] > max_y: max_y = self.line_top_l[i][1]
		for i in range(min_y,max_y+1): #Set min_x and max_x for each column y
			up.append(max_constant)
			down.append(0)
		for i in range(len(self.line_top_l)): #Get min_x and max_x for each column y
			if self.line_top_l[i][0] < up[self.line_top_l[i][1]-min_y]: up[self.line_top_l[i][1]-min_y] = self.line_top_l[i][0]
			if self.line_bottom_l[i][0] > down[self.line_top_l[i][1]-min_y]: down[self.line_top_l[i][1]-min_y] = self.line_bottom_l[i][0]
		for y in range(min_y,max_y+1):
			for x in range(up[y-min_y],down[y-min_y]+1):
				if self.pix.has_key((x,y)):
					self.line_pix[(x,y)] = self.pix[(x,y)]

	def get_line_tb(self,line):
		#get the top line
		for n in range(len(line)):
			up = 0
			if self.bs/2 == math.ceil(self.bs/2): #even
				up = self.bs/2 - 1
			else:
				up = math.ceil(self.bs/2) - 1
			self.line_top_l.append((line[n][0]-up,line[n][1]))
			if self.pix.has_key((line[n][0]-up,line[n][1])):
				self.line_top[(line[n][0]-up,line[n][1])] = self.pix[(line[n][0]-up,line[n][1])]
			else:
				self.line_top[(line[n][0]-up,line[n][1])] = (0,0,0)
		#get the bottom line
		for n in range(len(line)):
			down = self.bs - up - 1
			self.line_bottom_l.append((line[n][0]+down,line[n][1]))
			if self.pix.has_key((line[n][0]+down,line[n][1])):
				self.line_bottom[(line[n][0]+down,line[n][1])] = self.pix[(line[n][0]+down,line[n][1])]
			else:
				self.line_bottom[(line[n][0]+down,line[n][1])] = (0,0,0)

	def brush(self,s,e):
		line = []
		slope_max = 1000
		if e[0] == s[0]: #Calcule the slope of the curve
			if e[1] > s[1]: slope = slope_max
			else: slope = -slope_max
		else:
			slope=(e[1]-s[1])/(e[0]-s[0])
		#the following needs to be modified to output two lists of line and calls the painting of curves
		if slope >= 1 or slope <= -1:
			delta = abs(e[1]-s[1])
			for i in range(delta+1): line.append((int(s[0]+round(i/slope)),int(s[1]+i)))
		else:
			delta = abs(e[0]-s[0])
			for i in range(delta+1): line.append((int(s[0]+i),int(s[1]+round(i*slope))))
		return line

	def get_point(self,s,e):
		point_list = []
		dis = math.sqrt((e[1]-s[1])**2+(e[0]-s[0])**2)
		interval_dis = int(math.floor(dis/self.wd)) # Number of mid-points in a curve
		interval_x = 0
		interval_y = 0
		if interval_dis > 0:
			interval_x = (e[0]-s[0])/interval_dis
			interval_y = (e[1]-s[1])/interval_dis
		point_list.append(self.adjust_point(s))
		for i in range(interval_dis-1):
			point_list.append(self.adjust_point((int(s[0]+(i+1)*interval_x),int(s[1]+(i+1)*interval_y))))
		point_list.append(self.adjust_point(e))
		return point_list



'''
	def render():
		count=0 #count the current coverage
		check_s=False #check the start pos
		check_e=False #check the end pos
		while (count < cov):
			print count
			while (check_s == False): #randomly create the start pos
				start_init=[random.randint(0,size[0]-1),random.randint(0,size[1]-1)]
				check_s=check(image,segment_edges,start_init)
			while (check_e == False): #randomly create the end pos
				end_init=[random.randint(0,size[0]-1),random.randint(0,size[1]-1)]
				check_e=check(image,segment_edges,end_init)	
			r=random.uniform(0,wr)
			theta=random.uniform(0,2*math.pi)
			start=[int(start_init[0]+round(r*math.cos(theta))),int(start_init[1]+round(r*math.sin(theta)))] #move start pos randomly in a circle of radius wr
			r=random.uniform(0,wr)
			theta=random.uniform(0,2*math.pi)
			end=[int(end_init[0]+round(r*math.cos(theta))),int(end_init[1]+round(r*math.sin(theta)))] ##move end pos randomly in a circle of radius wr
			print r,theta		
			print start,end
			count=count+brush(image,start,end) #paint the cureve and count the coverage
		
	def check(image,edges,pos):
		count = 0 #count the number of edges
		#if image[pos[0]][pos[1]] != 0:
		#	return False
		#if edges[pos[0]][pos[1]] == True:
		#	return True

		#if number of edges on the same row or column of the point towards four directions respectively are all odd, the point is in the segment
		#otherwise, the point is out of the segment
		for i in range(pos[0]): #check the up direction
			if edges[i][pos[1]] == 1:
				count = count + 1
		if count % 2 == 0:
			return False
		count=0
		for i in range(len(edges)-pos[0]): #check the down direction 
			if edges[len(edges)-1-i][pos[1]] == 1:
				count = count + 1
		if count % 2 == 0:
			return False
		count=0
		for i in range(pos[1]): #check the left direction
			if edges[pos[0]][i] == 1:
				count = count + 1
		if count % 2 == 0:
			return False
		count=0
		for i in range(len(edges[0])-pos[1]): #check the right direction
			if edges[pos[0]][len(edges[0])-1-i] == 1:
				count = count + 1
		if count % 2 == 0:
			return False
		return True
'''
				
if __name__=="__main__":
	im = Image.new("RGB", (400, 400), (255, 255, 255))
	for i in range(19):
    			k = 20*(i+1)
   			for j in range(400):
        			im.putpixel((k, j),(0, 0, 0))
        			im.putpixel((j, k), (0, 0, 0))
	#image = [[0 for col in range(200)] for row in range(200)]
	#segment_edges = [[False for col in range(20)] for row in range(20)]
	edges = []	
	for i in range(100):
		edges.append((50+i,50))
		edges.append((150,50+i))
		edges.append((150-i,150))
	for i in range(30):
		edges.append((50,150-i))
		edges.append((50,51+i))
	for i in range(40):
		edges.append((50+i,120))
		edges.append((50+i,80))
		edges.append((90,120-i))
	edges.sort()
	for i in range(len(edges)):
		plt.scatter(edges[i][0],edges[i][1],color="red")
	fig1 = plt.figure()	
	pix = {}
	for x in range(50,151):
		for y in range(50,151):
			pix[(x,y)]=(255,0,0)
	seg_layer = Seg_layer(edges,pix,fig1,im)
	seg_layer.render(0)
	plt.show()
	im.show()
	#fig1.savefig('rect2.png', dpi=90, bbox_inches='tight')
	
	#render(image,segment_edges,wd,wr,cov)
	#plt.imshow(image)
	#plt.show()

