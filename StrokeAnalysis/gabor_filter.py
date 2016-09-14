from skimage.filters import gabor
from skimage import data, io
from matplotlib import pyplot as plt  
import numpy as np
import math
#image = data.coins()



class frequency:
	def __init__(self, image):
		self.e_i_list = []
		self.image = image
		
	def calcul(self):
		for i in range(7):
			freq=0.08-(0.01*(i+1))
			#print freq
			e_ij=[]#a list of imgs
			for j in range(8):#j is theta
				thet=j/8*math.pi
				e_j=np.ndarray(self.image.shape)#img (3)		
				filt_real, filt_imag = gabor(self.image, frequency=freq,theta=thet,sigma_x=1,sigma_y=1)
				for y in range(filt_real.shape[0]):
					for x in range(filt_real.shape[1]):
						e_j[y][x]=math.sqrt(filt_real[y][x]**2+filt_imag[y][x]**2)
				#io.imshow(e_j)
				#io.show()
				e_ij.append(e_j)
			e_i=np.ndarray(e_ij[0].shape)
			emax=0
			emin=255
			for y in range(e_ij[0].shape[0]):
				for x in range(e_ij[0].shape[1]):
					e_ijmax=0
					e_ijmaxindex=0
					for n in range(len(e_ij)):
						if e_ij[n][y][x]>e_ijmax:
							e_ijmax=e_ij[n][y][x]
							e_ijmaxindex=n
					if e_ijmaxindex==0:
						e_i[y][x]=e_ijmax+e_ij[7][y][x]+e_ij[e_ijmaxindex+1][y][x]
					elif e_ijmaxindex==7:
						e_i[y][x]=e_ijmax+e_ij[e_ijmaxindex-1][y][x]+e_ij[0][y][x]
					else:
						e_i[y][x]=e_ijmax+e_ij[e_ijmaxindex-1][y][x]+e_ij[e_ijmaxindex+1][y][x]
					if e_i[y][x]>emax:
						emax=e_i[y][x]
					if e_i[y][x]<emin:
						emin=e_i[y][x]

			for y in range(e_i.shape[0]):
				for x in range(e_i.shape[1]):
					e_i[y][x]=(e_i[y][x]-emin)*255/(emax-emin)
			self.e_i_list.append(e_i)
			ee_i=np.uint8(e_i)
			'''	
			plt.figure()
			io.imshow(ee_i)    
			io.show()  
			'''	
		return self.e_i_list


'''			
e_i=np.uint8(e_i)
plt.figure()            
io.imshow(e_i)    
io.show()               
'''
