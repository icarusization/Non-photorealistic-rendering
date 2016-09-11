import numpy as np
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.image import grid_to_graph
from skimage.filters import sobel,roberts,scharr,prewitt
from skimage.feature import canny
from Utility import *
from Segment import *
from skimage import io
from collections import deque
import matplotlib.pyplot as plt

#images={'sun','cloud','icarus'}
class Segmentation:
    def __init__(self):
        self.im=None #the original image
        self.no=1#number of objects
        self.ns=10#number of segments in each object
        self.lad=1#the lower bound for the abstraction levels
        self.wad=10#the upper bound for the abstraction levels
        self.es=3 #the weight for abstraction
        self.np=3 #number of pixels to smooth the boundary
        self.background=None
        self.objects=[]
        
    def imread(self,im):
        self.im=plt.imread(im)

    def set_no(self,no):
        self.no=no
        for i in range(self.no+1):#includeing the background segment
            tmp=Segment()
            self.objects.append(tmp)

    def set_ns(self,ns):
        self.ns=ns

    def set_abstraction(self,lad,wad):
        self.lad=lad#the maximum abstraction level
        self.wad=wad#the minimum abstraction level

    def set_es(self,es):
        self.es=es

    def set_np(self,np):
        self.np=np


    def breadthfirst(self,start,object_edges,edgelist,edgeset,i,queue):
        edgelist.append(start)
        edgeset.add(start)
        scanner=Neighbourscanner()
        f=lambda x:((x[0],x[1]) not in edgeset) and object_edges[x[0],x[1]]
        while(len(queue)):
            new_point=queue[0]
            queue.popleft()
            nb=scanner.neighbour(new_point[0],new_point[1],f)
            if(nb):
                for n in nb:
                    edgelist.append(n)
                    edgeset.add(n)
                    queue.append(n)


    def segment(self):
        height=self.im.shape[0]
        width=self.im.shape[1]
        data=np.ndarray(shape=(width*height,3), dtype=int)
        for row in range(height):
            for col in range(width):
                num=row*width+col
                data[num,0:3]=self.im[row][col]
        #The First Segmentation
        connectivity = grid_to_graph(self.im.shape[0],self.im.shape[1])
        ward = AgglomerativeClustering(n_clusters=self.no+1, linkage='ward',connectivity=connectivity)
        ward.fit(data)

        #Preparation for edge detection
        object_seg=np.ndarray(shape=(height,width,3),dtype=int)
        for row in range(height):
            for col in range(width):
                num=row*width+col
                label=ward.labels_[num]
                object_seg[row,col]=(255-label*50,255-label*50,255-label*50)
        objectbw=rgb2gray(object_seg)
        object_edges =  sobel(objectbw)
        #io.imshow(object_edges)
        #io.show()

        # Store the segments in objects
        counter=set()
        for row in range(height):
            for col in range(width):
                num=row*width+col
                label=ward.labels_[num]
                self.objects[label].pix[(row,col)]=self.im[row][col]
                if(object_edges[row,col]):
                    coord=(row,col)
                    nb=neighbour(row,col,height,width)
                    s=set()
                    for i in nb:
                        l=ward.labels_[i[0]*width+i[1]]
                        s.add(l)
                        counter.add(l)
                    for j in s:
                        self.objects[j].edge.append(coord)

        avg=np.empty(self.no+1)

        size=[]#to calculate the abstraction level
        for i in range(self.no+1):
            self.objects[i].size=len(self.objects[i].pix)
            self.objects[i].subsegment=[None for j in range(self.ns)]
            pixarray=np.array(list(self.objects[i].pix.values()))
            avg[i]=np.mean(pixarray)
	    self.objects[i].avg_color=avg[i]
            size.append(self.objects[i].size)
        #pick out the background
        bg=avg.argmax(axis=0)
        self.background=self.objects[bg]
        del self.objects[bg]
        del size[bg]

        '''
        #store the edges
        for i,ob in enumerate(self.objects):
            start=ob.edge[0]
            edgelist=[]
            edgeset=set()
            queue=deque()
            queue.append(start)
            self.breadthfirst(start,object_edges,edgelist,edgeset,i,queue)
            self.objects[i].edge=edgelist
        '''

        #calculate the abstraction level
        L=max(size)
        M=min(size)
        for i in range(self.no):
            r=self.objects[i].size
            #self.objects[i].abstraction_level=int(self.wad+(r-M)/(L-M)*(self.lad-self.wad))
            self.objects[i].abstraction_level=10


        #show the edges
        for ob in self.objects:
            #ob.abstract(self.es)
            object_edge=np.zeros(shape=(height,width),dtype=np.uint8)
            for e in ob.edge:
                object_edge[e[0],e[1]]=1
            #io.imshow(object_edge)
            #io.show()


        #The Second Segmentation
        #Store the segmentation result in the subsegment list(with pix,edges)
        result=np.zeros(shape=(len(self.objects),height,width,3),dtype=np.uint8)
        for i,ob in enumerate(self.objects):
            data=np.array(ob.pix.values())
            location=np.array(ob.pix.keys())
            #connectivity matrix for structured Ward
            connectivity=kneighbors_graph(location,n_neighbors=10,include_self=False)
            # make connectivity symmetric
            connectivity = 0.5 * (connectivity + connectivity.T)
            ward = AgglomerativeClustering(n_clusters=self.ns, linkage='ward',connectivity=connectivity,n_components=self.ns+1)
            ward.fit(data)
            #redraw the segments
            #create a dictionary for later labelling
            label_dict={}
            for j,p in enumerate(ob.pix.keys()):
                label=ward.labels_[j]
                label_dict[p]=label
                result[i,p[0],p[1]]=(255-label*15,255-label*15,255-label*15)
            segmentbw=rgb2gray(result[i])
            segment_edges = sobel(segmentbw)
        

            #plt.imshow(result[i])
            #plt.show()
            #io.imshow(segment_edges)
            #io.show()


            # Store the subsegments and their edges in the subsegment list
            #create a subsegment list
            subpix=[{} for ii in range(self.ns)]
            subedge=[[] for ii in range(self.ns)]
            for k,p in enumerate(ob.pix.keys()):
                label=ward.labels_[k]
                subpix[label][p]=ob.pix[p]
                row=p[0]
                col=p[1]
                if(segment_edges[row,col]):
                    
                    nb=neighbour(row,col,height,width)
                    s=set()
                    for l in nb:
                        if(label_dict.has_key(l)):
                            lab=label_dict[l]
                            s.add(lab)
                    for m in s:
                        subedge[m].append((row,col))  
            

            size=[]
            for n in range(self.ns):
                tmp=Segment()
                tmp.pix=subpix[n]
		pixarray=np.array(tmp.pix.values())
		tmp.avg_color=np.mean(pixarray)
                tmp.size=len(subpix[n])
                tmp.edge=subedge[n]
                #print n
                self.objects[i].subsegment[n]=tmp
                size.append(tmp.size)


            '''
            #calculate the abstraction level
            L=max(size)
            M=min(size)
            self.objects[i].L=L
            self.objects[i].M=M
            for ii in range(self.ns):
                r=ob.subsegment[ii].size
                ab=self.wad+(r-M)/(L-M)*(self.lad-self.wad)
                self.objects[i].subsegment[ii].abstraction_level=int(ab)
            '''

if __name__=="__main__":
    sg=Segmentation()
    sg.imread("input.jpg")
    sg.set_no(3)
    sg.set_ns(10)
    sg.set_abstraction(1,10)
    sg.set_es(1)
    sg.segment()
