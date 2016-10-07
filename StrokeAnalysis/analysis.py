from skimage.filters import gabor
from skimage import data, io
from matplotlib import pyplot as plt  
import numpy as np
import math
import gabor_filter
import multi_orientation

class pixel:
	def __init__(self,p):
		self.h = p[0]
		self.s = p[1]
		self.v = p[2]
		self.cluster = -1

	def colordiff(self,s):
		return math.sqrt((self.h-s[0])**2+(self.s-s[1])**2+(self.v-s[2])**2)	

class color:
	def __init__(self):
		self.h = 0
		self.s = 0
		self.v = 0
		self.hssr=0
		self.sssr=0
		self.vssr=0
		

class stroke_analysis:
	def __init__(self, graph, cmap):
		self.graph = graph # HSV graph
		self.cmap = cmap
		self.color_difference_threshold = 40
		self.color_N_thredhold = 100
		self.size = self.graph.shape
		self.color_list = []
		self.p_list = []#point sets

	def visibilty(self):
		thredhold = 25
		count = 0
		sum = 0
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				if self.graph[x][y] > thredhold:
					count++
					sum+=self.graph[x][y]
		S_T = sum/count
		return S_T

	def density_connect(self,cluster_number,p):
		for i in range(len(self.p_list))
			d = self.p_list[i]
			if d.cluster == -1:
				diff = d.colordiff(d,p)
				if diff < self.color_difference_threshold:
					self.p_list[i].cluster=cluster_number
					self.density_connect(cluster_number,self.p_list[i])


	def color_cluster(self):
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				t = pixel(self.graph[x][y])
				self.p_list.append(t)
		cluster_number = 0
		for i in range(len(self.p_list)):
			if self.p_list[i].cluster==-1:
				cluster_number++
				self.p_list[i].cluster=cluster_number
				self.density_connect(cluster_number,self.p_list[i])
		for j in range(cluster_number):
			color_l = []
			self.color.append(color_l)

		for k in range(len(self.p_list)):
			n = self.p_list[k].cluster
			self.color[n].append(self.p_list[k])

	def color_analysis(self):
		c_list=[]
		for i in range(len(self.color)):
			l = len(self.color[i])
			
			if l>self.color_N_thredhold:
				sumh = 0
				sums = 0
				sumv = 0
				for j in range(l):
					sumh+=self.color[i][j][0]
					sums+=self.color[i][j][1]
					sumv+=self.color[i][j][2]

				avh = sumh/l
				avs = sums/l
				avv = sumv/l

				SSRh=0
				SSRs=0
				SSRv=0
				for j in range(l):
					SSRh+=(self.color[i][j][0]-avh)**2
					SSRs+=(self.color[i][j][1]-avs)**2
					SSRv+=(self.color[i][j][2]-avv)**2
				SSRh/=l
				SSRs/=l
				SSRv/=l
				c=color()
				c.h=avh
				c.s=avs
				c.v=avv
				c.hssr=SSRh
				c.sssr=SSRs
				c.vssr=SSRv
				c_list.append(c)
		return c_list		