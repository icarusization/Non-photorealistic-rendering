from Neighborhood import *
import scipy.misc
from matplotlib import pyplot as plt
from ReactionDiffusion import *
from Strokes import *
import numpy as np
from time import *

def gradient_descent(origin_list,reference_list,neighbour,center,lam):
    l=len(origin_list)
    print ("reference")
    print reference_list[0:5]
    print ("origin")
    print origin_list[0:5]
    for i in range(100):
	new_list=[]
    	for k in range(l):
    		r=np.sin(reference_list[k]-origin_list[k])
		d=0
    		for n in range(len(neighbour[k])):
    			distance=(float)(np.sqrt((center[neighbour[k][n]][0]-center[k][0])**2
                                         +(center[neighbour[k][n]][1]-center[k][1])**2))
    			w=(float)(1/distance)
    			d=d+w*np.sin(origin_list[neighbour[k][n]]-origin_list[k]) 
    		d_o=r+lam*d+0.001
    		o=origin_list[k]-0.01*d_o
		while o>=2*3.1415926:
			o=o-2*3.1415926
		while o<0:
			o=o+2*3.1415926
    		new_list.append(o)

     	print("newlist")
     	print new_list[0:5]
    	for k in range(l):
    		origin_list[k]=new_list[k]
  

	

class Painter:
    def __init__(self):
        #the reference maps
        self.segmentation_map=None
        self.saliency_map=None
        self.density_map=None
        self.orientation_field=None
        self.size_map=None
        self.color_map=None
        #the corresponding neighborhood graph
        self.neighborhood_graph=None
        #the parameters
        self.density=1.0
        self.non_uniformity=1.0
        self.local_isotropy=1.0
        self.coarseness=1.0
        self.size_contrast=1.0
        self.light_contrast=1.0
        self.chroma_contrast=1.0
        self.hue_contrast=1.0
        #the final strokes
        #[[orientation,size,color(hsv)],...]
        self.orientationlist=None
        self.sizelist=None
        self.colorlist=None

    def set_colormap(self):
        colormap=plt.imread("123.png")
        self.colormap=colormap[:,:,0:3]

    def construct_neighbor(self):
        print   "Begin constructing neighborhood graph:"
        nb=Neighborhood()
        dm=scipy.misc.imread("density.png").astype(np.float)
        #dm=plt.imread("density.png")
        nb.set_density(0.5)
        nb.set_densitymap(dm)
        nb.sample()
        self.strokelist=[[] for i in range(len(nb.samplelist))]
        im=scipy.misc.imread("edge.png").astype(np.float)
        #im=plt.imread("edge.png")
        nb.set_image(im)
        nb.set_iternum(50)
        nb.set_orientation()
        nb.construct_gragh()
        self.neighborhood_graph=nb
        print 50*"-"


    def orientation_diffusion(self):
        t=time()
        ord=ReactionDiffusion()
        ord.set_diffusion(0.1)
        ord.set_iternum(50)
        ord.set_mode(0)
        ord.set_reaction(self.neighborhood_graph.orientationlist)
        ord.set_neighbor(self.neighborhood_graph.neighborhood_graph)
        ord.diffusion()
        self.orientationlist=ord.result
   	#self.orientationlist=self.neighborhood_graph.orientationlist
	gradient_descent(self.orientationlist,self.neighborhood_graph.orientationlist,
                        self.neighborhood_graph.neighborhood_graph,self.neighborhood_graph.samplelist,8)
        print "Orientation diffusion", time()-t
        #update the neighborhood graph
        #self.neighborhood_graph.update_graph(ord.result)
    	self.neighborhood_graph.update_graph(self.orientationlist)


    def size_diffusion(self):
        t=time()
        #the refernce value: RANDOM NOW!!!!!!!!!!!!!!!!!!!!
        lengthreference=[10+np.random.randint(5)
                       for i in range(len(self.neighborhood_graph.samplelist))]
        lrd=ReactionDiffusion()
        lrd.set_diffusion(1.0)
        lrd.set_iternum(50)
        lrd.set_mode(0)
        lrd.set_reaction(lengthreference)
        lrd.set_neighbor(self.neighborhood_graph.neighborhood_graph)
        lrd.diffusion()
        widthreference=[5+np.random.randint(3)
                        for i in range(len(self.neighborhood_graph.samplelist))]
        wrd=ReactionDiffusion()
        wrd.set_diffusion(1.0)
        wrd.set_iternum(50)
        wrd.set_mode(0)
        wrd.set_reaction(widthreference)
        wrd.set_neighbor(self.neighborhood_graph.neighborhood_graph)
        wrd.diffusion()
        self.sizelist=zip(lrd.result,wrd.result)
        print "Size diffusion", time()-t

    def color_diffusion(self):
        t=time()
        #reference color at the sample points
        reference=[]
        for sample in self.neighborhood_graph.samplelist:
            color=self.colormap[sample[0],sample[1]]
            tmp=Color(color[0],color[1],color[2])
            reference.append([tmp.H,tmp.S,tmp.V])
        crd=ReactionDiffusion()
        crd.set_diffusion(1.0)
        crd.set_iternum(50)
        crd.set_mode(1)
        crd.set_reaction(reference)
        crd.set_neighbor(self.neighborhood_graph.neighborhood_graph)
        crd.diffusion()
        self.colorlist=crd.result
        print "Color diffusion", time()-t


    def paint(self):
        t=time()
        #Create an initial instance of stroke
        s = Stroke()
        # Here you can revise these parameters according to the introduction in the Strokes Class.
        s.distort = 0.2
        s.shake = 0.3
        s.tapering = 0.5
        s.ColorVariability = 0.5
        s.ShadeVariability = 0.5

        #The array to store the final painting
        height,width,_=self.colormap.shape
        painting=np.ndarray(shape=(height,width,3))

        #construct the stroke list
        #[[(x1,y1),[x2,y2],w,rgb],...]
        #What we have: samplelist(centerlist),orientaionlist,sizelist,colorlist
        for i in range(len(self.orientationlist)):
            center=self.neighborhood_graph.samplelist[i]
            center=[center[0]+0.5,center[1]+0.5]
            c=Color()
            c.give_color(self.colorlist[i][0], self.colorlist[i][1], self.colorlist[i][2])
            s.color=c
            orientation=self.orientationlist[i]
            l,w=self.sizelist[i]
            #claculate the two mid points of the two ends of a stroke
            leftend=[int(center[0]-np.cos(orientation)*l),int(center[1]-np.sin(orientation)*l)]
            rightend=[int(center[0]+np.cos(orientation)*l),int(center[1]+np.sin(orientation)*l)]
            points = s.draw_strokes(leftend[0], leftend[1], rightend[0], rightend[1], w, s.color)

            for i in range(len(points)):
                p = points[i]
                c = p[2]
                nc = c.get_color()
                nc = (int(nc[0] * 255), int(nc[1] * 255), int(nc[2] * 255))
                #print nc
                if 0<=p[0]<height and 0<=p[1]<width:
                    painting[p[0], p[1]]= nc
        print "Painting", time()-t
        #plt.imshow(painting)
        #plt.show()
        scipy.misc.imsave("masterpice.jpg",painting)


if __name__=="__main__":
    pt=Painter()
    pt.set_colormap()
    pt.construct_neighbor()
    pt.orientation_diffusion()
    pt.size_diffusion()
    pt.color_diffusion()
    pt.paint()
    #listo=[0.02, 0.03, 0.04, 0.01, 0.05, 0.06, 0.08]
    #listr=[3, 5, 6, 1, 2, 4, 8]
    #listn=[[1, 2],[2],[3],[2, 4],[5],[4],[0, 2]]
    #center=[(0,0),(1,1),(3,2),(4,4),(5,5),(2,3),(2,1)]
    #gradient_descent(listo,listr,listn,center,1.0)
