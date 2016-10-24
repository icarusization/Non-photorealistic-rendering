from Orientation import *
import numpy as np
#import matplotlib.pyplot as plt
import scipy.misc
import numpy.linalg as LA
from time import *

def neighbour(row,col,height,width):
    #row,col is the coordinate of the pixel, while height,width is the dimension of the image
    #return the coordinates of the neighboring pixels
    neighbour=[(i,j) for i in range(row-1,row+2) for j in range(col-1,col+2)]
    neighbour=filter(lambda x:x[0]>=0 and x[0]<height and x[1]>=0 and x[1]<width, neighbour)
    neighbour.remove((row,col))
    return neighbour

class Neighborhood:
	def __init__(self):
		self.density=None
		self.densitymap=None
		self.im=None
		self.orientaion=None
		self.samplemap=None
		self.samplelist=None #the samples
		self.orientationlist=None #the orientations at the samples
		self.distmat=None #to cache the distance matrix for later use
		self.neighborhood_graph=None #the final result

	def set_image(self,im):
		self.im=im

	def set_density(self,d):
		self.density=d

	def set_iternum(self,num):
		#set the iteration number for the reference orientation map
		self.iternum=num

	def set_densitymap(self,m):
		self.densitymap=m[:,:,0]
		height,width=self.densitymap.shape
		self.samplemap=np.zeros(shape=(height,width))

	def set_orientation(self):
		#set the orientation reference
		t=time()
		o=Orientation()
		o.set_image(self.im)
		o.set_iternum(self.iternum)
		o.diffusion()
		self.orientation=o
		print "Orientation",time()-t


	def sample(self):
		t=time()
		self.samplelist=[]
		windowsize=(10,10)
		height,width=self.densitymap.shape
		vstride=int(height/windowsize[0])
		hstride=int(width/windowsize[1])
		for i in range(vstride):
			for j in range(hstride):
				topleft=(windowsize[0]*i,windowsize[1]*j)
				window=self.densitymap[topleft[0]:(topleft[0]+windowsize[0]),topleft[1]:(topleft[1]+windowsize[1])]
				meandensity=np.mean(window)/255
				#meandensity=19.87
				samplenum=int(1+5*self.density*(np.exp(meandensity)-1))
				sample=np.random.choice(windowsize[0]*windowsize[1],samplenum,replace=False)
				samplepixel=map(lambda x:(x/windowsize[1],x%windowsize[1]),sample)
				for px in samplepixel:
					pos=(topleft[0]+px[0],topleft[1]+px[1])
					nb=neighbour(pos[0],pos[1],height,width)
					rejected=False
					for n in nb:
						if(self.samplemap[n[0],n[1]]):
							rejected=True
					if(rejected==False):
						self.samplemap[pos[0],pos[1]]=1
						self.samplelist.append((pos[0],pos[1]))
		print "Sampling", time()-t
		#plt.imshow(self.samplemap)
		#plt.show()


	def construct_gragh(self):
		#construct the distance map
		t=time()
		numsamples=len(self.samplelist)
		distmat=np.ndarray(shape=(numsamples,numsamples))
		for i in range(numsamples):
			for j in range(numsamples):
				distmat[i,j]=LA.norm(np.array(self.samplelist[i])-np.array(self.samplelist[j]))
		distmat=np.argsort(distmat, axis=1,kind='heapsort')
		self.distmat=distmat
		self.orientationlist=[]
		for sample in self.samplelist:
			self.orientationlist.append(self.orientation.dic[sample][0])
		#The neighborhood graph: n*4
		#First, for each sample find the nearest 10 samples
		#Next, construct a local coordinate systerm, fill the samples in each quadrant
		#Finally, connect the sample to the nearest sample in each quadrant
		self.neighborhood_graph=[[] for i in range(len(self.samplelist))]
		for i in range(len(self.samplelist)):
			sample=self.samplelist[i]
			orientation=self.orientationlist[i]
			f1=lambda x: (x[1]-sample[1])-np.tan(orientation)*(x[0]-sample[0])>0
			f2=lambda x: (x[1]-sample[1])+1.0/(np.tan(orientation)+0.001)*(x[0]-sample[0])>0
			s0=s1=s2=s3=False
			for j in range(1,11):
				#the 1st one is itself
				nb=self.samplelist[distmat[i,j]]
				if(s0 and s1 and s2 and s3):
					break
				if(not s0 and not f1(nb) and not f2(nb)):
					s0=True
					self.neighborhood_graph[i].append(distmat[i,j])
				if(not s1 and not f1(nb) and f2(nb)):
					s1=True
					self.neighborhood_graph[i].append(distmat[i,j])
				if(not s2 and f1(nb) and not f2(nb)):
					s2=True
					self.neighborhood_graph[i].append(distmat[i,j])
				if(not s3 and f1(nb) and f2(nb)):
					s3=True
					self.neighborhood_graph[i].append(distmat[i,j])
		print "Neighborhood graph construction", time()-t
		#haven't considered boundaries yet

	def update_graph(self,new_orientations):
		t=time()
		self.neighborhood_graph=[[] for i in range(len(self.samplelist))]
		for i in range(len(self.samplelist)):
			sample=self.samplelist[i]
			orientation=new_orientations[i]
			f1=lambda x: (x[1]-sample[1])-np.tan(orientation)*(x[0]-sample[0])>0
			f2=lambda x: (x[1]-sample[1])+1.0/(np.tan(orientation)+0.001)*(x[0]-sample[0])>0
			s0=s1=s2=s3=False
			for j in range(1,11):
				#the 1st one is itself
				nb=self.samplelist[self.distmat[i,j]]
				if(s0 and s1 and s2 and s3):
					break
				if(not s0 and not f1(nb) and not f2(nb)):
					s0=True
					self.neighborhood_graph[i].append(self.distmat[i,j])
				if(not s1 and not f1(nb) and f2(nb)):
					s1=True
					self.neighborhood_graph[i].append(self.distmat[i,j])
				if(not s2 and f1(nb) and not f2(nb)):
					s2=True
					self.neighborhood_graph[i].append(self.distmat[i,j])
				if(not s3 and f1(nb) and f2(nb)):
					s3=True
					self.neighborhood_graph[i].append(self.distmat[i,j])
		print "Neighborhood graph updated", time()-t


if __name__=="__main__":
	nb=Neighborhood()
	dm=scipy.misc.imread("density.png").astype(np.float)
	#dm=plt.imread("density.png")
	nb.set_density(0.5)
	nb.set_densitymap(dm)
	nb.sample()
	im=scipy.misc.imread("edge.png").astype(np.float)
	#im=plt.imread("edge.png")
	nb.set_image(im)
	nb.set_iternum(1)
	nb.set_orientation()
	nb.construct_gragh()
