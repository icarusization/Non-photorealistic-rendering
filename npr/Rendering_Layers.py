import numpy as np
import random as rd
from skimage import io,data
from Utility import *
from Segment import *
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import math

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v


CAM_CLOSED = 0
CAM_RANDOM = 1

palette_color = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,255),(255,255,255),(0,0,0),(255,125,0),(255,218,185),(47,79,79),(119,136,153),(105,105,105),(25,25,112),(65,105,225),(0,191,255),(143,188,143),(32,178,170),(50,205,50),(250,250,210),(238,221,130),(188,143,143),(205,133,63),(210,105,30),(165,42,42),(255,165,0),(240,128,128),(255,20,147),(176,48,96),(186,85,211),(148,0,211),(147,112,219),(108,123,139),(155,48,255)]
default_palette_color = [(0,0,0),(60,0.7,1),(120,1,0.5),(180,0.26,0.93),(240,0.78,0.44),(300,0.45,0.93),(355,0.83,0.89)]

# Create Layer class:
# Function: 
#   To rend all the segments using the colors we have in our palette.

# Input from GOD layer:
#   segs: A list of class "Segment" in "Utility.py"

# Output to segment layer:
#   edges: A list of pixels(only locations) which are the edges of a segment.
#   pixels: A list of all the pixels in a segment.

class Layers:
    def __init__(self):
        self.segs = None                #   segs: A list of class "Segment" in "Utility.py".
        self.noc = 20                   #   noc:  The maximum number of the colors which will appear in the rendering.
        self.pc = default_palette_color #   pc:   Palette constraints. It indicates which colors in the palette are allowed.
        self.cam = CAM_CLOSED           #   cam:  Color assignment method. 
        self.vib = 0.05                 #   vib:  Random process in color assignment.  
        self.inv = 0.05                 #   inv:  Inverse_color_ration.

    def set_segs(self, segs):
        self.segs = segs

    def set_noc(self, noc):
        self.noc = noc

    def set_pc(self, pc):
        self.pc = pc
    
    def set_cam(self, cam):
        self.cam = cam 
    
    def set_vib(self, vib):
        self.vib = vib

    def set_rev(self, rev):
        self.rev = rev

################################## main process
    def rendering(self):
        for obj in self.segs:
            obj.subsegment = self.reorder(obj)
            for i in range(len(obj.subsegment)):
                seg = obj.subsegment[i]
                ss = len(seg.pix)
                mc = get_mean(seg.pix)
        # decide which color shall be used
                self.assign_color(seg, self.vib, self.rev, mc, ss)
        # carry out the segment rendering 
                # rd_sg(seg.pix, seg.edge)
                # rd_sg.rendering()
###########################################

    def assign_color(self, seg, vib=0, rev=0, mc=0, ss=0): #style of strategy we used 
        if(self.cam == CAM_CLOSED): 
            for pos, pix in seg.pix.items():
                seg.pix[pos] = self.closed_assign(pix,vib,rev);
        if(self.cam == CAM_RANDOM):
            seg_mean = self.random_assign(vib,rev,mc,ss)
            for pos, pix in seg.pix.items():
                seg.pix[pos] = [pix[i]*0.5+seg_mean[i]*0.5 for i in range(3)];

    def closed_assign(self,pix,vib,rev):
        closed_pix,closed_dif = -1,-1
        for index, ppix in enumerate(palette_color):
            vib_pix = [ppix[i]*rd.uniform(1-vib,1+vib) for i in range(3)]
            if rd.random()<rev:
                vib_pix[0] = (vib_pix[0]+180)%360
            dif = sum([(vib_pix[i]-pix[i])*(vib_pix[i]-pix[i]) for i in range(3)])
            if closed_pix == -1 or (closed_dif !=-1 and dif<closed_dif):
                closed_dif,closed_pix = dif, index
        as_color = palette_color[closed_pix]
        pix[0:3] = [as_color[0],as_color[1],as_color[2]]
        return pix

    def random_assign(self,vib,rev,mc,ss):
        as_color = palette_color[rd.randint(0,len(palette_color)-1)]
   
        pix = [as_color[i]*rev*10+mc[i]*(1-rev) for i in range(3)]
        return pix

    def reorder(self, segs):
    # sort segments from the smallest to largest according to their pixels size
        size_list = []
        for index, seg in enumerate(segs.subsegment):
            size = len(seg.pix)
            size_list.append([size,index])
        size_list.sort()
        orderd_pixs = [segs.subsegment[size_list[i][1]] for i in range(len(segs.subsegment))]
        return orderd_pixs

    def set_pc(self):
        i=0
        for s in self.segs:
            for k in s:
                i=i+1
                if i==1:
                    iarray=np.array([[s[k][0],s[k][1],s[k][2]]])
                else:
                    v=np.array([[s[k][0],s[k][1],s[k][2]]])
                    iarray=np.vstack((iarray,v))
        kmeans = KMeans(n_clusters=self.noc, random_state=0).fit(iarray)
        colors=kmeans.cluster_centers_
        self.pc=[]
        for k in colors:
            if len(self.pc)==0:
                h,s,v=rgb2hsv(k[0],k[1],k[2])
                self.pc.extend([h,s,v])
            else:
                h,s,v=rgb2hsv(k[0],k[1],k[2])
                hmax=0
                for n,value in enumerate(self.pc):
                    if h<value[0]:
                        self.pc.insert(n,[h,s,v])
                        break
                    elif n==len(self.pc)-1:
                        self.pc.insert(n+1,[h,s,v])
                        break

                    


def findscale(out):
    i=len(out)
    xmax=0
    ymax=0
    xmin=999999999
    ymin=999999999
    for k in out:
        if k[0]>xmax :
            xmax=k[0]
        if k[0]<xmin :
            xmin=k[0]
        if k[1]>ymax :
            ymax=k[1]
        if k[1]<ymin :
            ymin=k[1]
    height=ymax-ymin+1
    width=xmax-xmin+1	
    height=int(height)
    width=int(width)
    return height,width,xmin,ymin


def segprint(out,canvas=None):
    z=0
    if canvas is None:
        height,width,xmin,ymin=findscale(out)
    else:
        height=canvas[0]
        width=canvas[1]
    height=int(height)
    width=int(width)
    result=np.empty((height,width,3))
    row =0
    col =0
    for row in range(height):
        for col in range(width):
            result[row][col][0]=255
            result[row][col][1]=0
            result[row][col][2]=255
    for k in out:
        if canvas==None:
            x=k[0]-xmin
            y=k[1]-ymin
        else:
            x=k[0]
            y=k[1]
        result[y][x]=[out[k][0],out[k][1],out[k][2]]
    result=np.uint8(result)
    #plt.imshow(result)
    #plt.show()

if __name__ == '__main__':
    #img = data.coffee()
    img = io.imread("input.jpg")
    img_pix = {}
    for c in range(img.shape[0]):
        for r in range(img.shape[1]):
            pos = (c,r)
            img_pix[pos] = img[c][r]
# set up a list of object
    seg_list = []
    seg = Segment()
    sub_seg = Segment()
    pixs = img_pix
    sub_seg.pix = pixs
    seg.subsegment.append(sub_seg)
    seg_list.append(seg)
# run
    ly = Layers()
    ly.set_segs(seg_list)
    ly.set_noc(10)
    ly.set_pc(palette_color)
    ly.set_cam(CAM_RANDOM)
    ly.set_vib(0.1)
    ly.set_rev(0.05)
    print len(ly.segs[0].subsegment)
    print "ORIGIN_COLOR"
    #for i in range(len(pixs)):
    #    print ly.segs.subsegment[0].pix.values()[i]
    print "AFTER_ASSIGNMENT"
    ly.rendering()
    #for i in range(len(pixs)):
    #    print ly.segs[0].subsegment[0].pix.values()[i]
    segprint(ly.segs[0].subsegment[0].pix)


