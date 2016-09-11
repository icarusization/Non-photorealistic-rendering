from skimage.filters import gabor
from skimage import data, io
from matplotlib import pyplot as plt  
import numpy as np
import math
import gabor_filter

class multi_orientation:
	def __init__(self, energy):
		self._lambda = math.sqrt(2)
		self.energy = energy
		self.size = self.energy[0].shape
		self.neigh_r = 2
		self.M = np.ndarray(self.size)
		self.MD = np.ndarray(self.size)
		self.S = np.ndarray(self.size)

	def sign(self, x):
		if x > 0:
			return 1
		else:
			return 0
	
	def on_image(self, pos):
		(x,y) = pos
		return x >= 0 and y >= 0 and x < self.size[0] and y < self.size[1]

	def mu(self, pos, Mi):
		(x,y) = pos
		M_mu = 0
		for i in range(-self.neigh_r, self.neigh_r+1):
			for j in range(-self.neigh_r, self.neigh_r+1):
				if self.on_image((x+i,y+j)) and i**2+j**2 <= self.neigh_r**2:
					M_mu += Mi[x+i][y+j]
		return M_mu
		
	def calcul_M(self):
		for i in range(6):
			Mi = np.zeros(self.size)
			for x in range(self.size[0]):
				for y in range(self.size[1]):
					diff = self.energy[i][x][y]-self.energy[i+1][x][y]
					Mi[x][y] = (diff)*self.sign(diff)
			for x in range(self.size[0]):
				for y in range(self.size[1]):
					self.M[x][y] += Mi[x][y]*self.mu((x,y), Mi)
		MM=np.uint8(self.M)
		print "M graph"
		plt.figure()            
		io.imshow(MM)    
		io.show()  
		

	def calcul_MD(self):
		e_ij = []
		for j in range(8):
			thet = j/8*math.pi
			e_j = np.ndarray(self.size)		
			filt_real, filt_imag = gabor(self.M, frequency=self._lambda, theta=thet, sigma_x=1, sigma_y=1)
			for y in range(filt_real.shape[0]):
				for x in range(filt_real.shape[1]):
					e_j[y][x]=math.sqrt(filt_real[y][x]**2+filt_imag[y][x]**2)
			e_ij.append(e_j)
		e_i=np.ndarray(e_ij[0].shape)
		for y in range(e_ij[0].shape[0]):
			for x in range(e_ij[0].shape[1]):
				e_ijmax=0
				e_ijmaxindex=0
				e_total = 0
				for n in range(len(e_ij)):
					e_total += e_ij[n][y][x]
					if e_ij[n][y][x]>e_ijmax:
						e_ijmax=e_ij[n][y][x]
						e_ijmaxindex=n
				#e_total = e_total/5
				if e_ijmaxindex==0:
					e_i[y][x]=e_ijmax+e_ij[7][y][x]+e_ij[e_ijmaxindex+1][y][x]
				elif e_ijmaxindex==7:
					e_i[y][x]=e_ijmax+e_ij[e_ijmaxindex-1][y][x]+e_ij[0][y][x]
				else:
					e_i[y][x]=e_ijmax+e_ij[e_ijmaxindex-1][y][x]+e_ij[e_ijmaxindex+1][y][x]
				self.MD[y][x] = (e_i[y][x]-(e_total-e_i[y][x])/7)/e_i[y][x]
		MMD=np.uint8(self.MD)

	def calcul_S(self):
		smax = 0
		smin = 99999999999999
		for x in range(2,self.size[0]-2):
			for y in range(2,self.size[1]-2):
				self.S[x][y] = self.MD[x][y]*self.mu((x,y),self.MD)
				if self.S[x][y] > smax:
					smax =  self.S[x][y]
				if self.S[x][y] < smin:
					smin =  self.S[x][y]
		band = smax - smin
		for x in range(self.size[0]):
			for y in range(self.size[1]):
				if x<=2 or y<=2 or x>=self.size[0]-3 or y>=self.size[1]-3:
					self.S[x][y] = 0
				else:
					self.S[x][y] = (smax - self.S[x][y])/band*255
				print self.S[x][y]
		SS=np.uint8(self.S)
		print "S graph"
		plt.figure()            
		io.imshow(SS)    
		io.show()  

if __name__=="__main__":
	image = io.imread('x.jpg',as_grey=True)
	image = np.uint8(image*255)
	#e_sp=np.ndarray(image.shape)
	f = gabor_filter.frequency(image)
	energy = f.calcul()
	o = multi_orientation(energy)
	o.calcul_M()
	o.calcul_MD()
	o.calcul_S()
