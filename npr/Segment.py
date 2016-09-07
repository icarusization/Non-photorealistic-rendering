from skimage.draw import bezier_curve,line
from skimage import io
import numpy as np

class Segment:
    def __init__(self):
        self.size=10
        self.edge=[]
        self.abstraction_level=0
        self.pix={}
	self.avg_color=(0,0,0)
        self.subsegment=[]
        self.L=50#the largest size of the subsegments
        self.M=0#the smallest size of the subsegments

    def abstract(self,es):
        #pick some points in the edge list, and reconnect the points by a quadratic bezier curve
        w=es#the weight to control the middle point
        defining_points=[]
        ab=self.abstraction_level
        for i,e in enumerate(self.edge):
            if(i%ab==0):
                defining_points.append(e)
        #defining_points.append(defining_points[0])
        results=[]
        start_point=0
        end_point=len(defining_points)-1-((len(defining_points)-1)%2)
        if(end_point!=len(defining_points)-1):
            last=defining_points[end_point:]
            defining_points.insert(len(defining_points)-1,[last[0][0],last[1][1]])

        for i in range(start_point,end_point,2):
            cpt=defining_points[i:i+3]
            rr, cc = bezier_curve(cpt[0][0],cpt[0][1],cpt[1][0],cpt[1][1],cpt[2][0],cpt[2][1],es)
            #print i,cpt
            #print i,zip(rr,cc)
            results+=zip(rr,cc)
        rr,cc=line(defining_points[end_point][0],defining_points[end_point][1],defining_points[start_point][0],defining_points[start_point][1])
        results+=zip(rr,cc)
        #delete the duplicate points
        final_results=list(set(results))
        #remain the previous order
        final_results.sort(key=results.index)
        self.edge=final_results


    def smooth(self,np):
        #smooth the boundery with the parameter np
        pass

if __name__=='__main__':
    sg=Segment()
    img=np.zeros(shape=(200,200))
    edge=[(60,j)for j in range(60,141)]
    edge+=[(i,140)for i in range(60,141)]
    edge+=[(140,j) for j in range(140,59,-1)]
    edge+=[(i,60)for i in range(140,59,-1)]
    sg.edge=edge
    sg.abstraction_level=8
    sg.abstract(1)
    for e in sg.edge:
        img[e[0],e[1]]=1
    io.imshow(img)
    io.show()

