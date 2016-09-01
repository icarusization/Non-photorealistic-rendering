#-*- coding:utf-8 -*-
import numpy as np
from Segmentation import *
from Rendering_Layers import *
#from transformation import *
from Render_segment_layers import *
from Canvas import *
import math
from skimage import io
import time


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


class Painter:
    def __init__(self,Seg=None,canvas=None):
        self.Segmentation = Seg
        self.Subsegs = []
        self.layers = None
        self.canvas =  canvas
        
              

    def set_Segmentation(self, segs):
        self.Segmentation = segs

    def set_Subsegs(self):
        for s in self.Segmentation.objects:
            for b in s.subsegment:
                bb=[b]
                self.Subsegs.extend(bb)

    def assigncolor(self):
        self.layers=Layers()
        self.layers.set_segs(self.Segmentation.objects)
        self.layers.set_noc(150)
        time1=time.time()
        #pc_list=self.layers.set_pc2(self.layers.pigments,self.layers.noc)
        #self.layers.set_pc(pc_list)
        self.layers.set_pc1()
        time2=time.time()
        print "set_pc done in ",time2-time1," s"
        self.layers.rendering()

    def set_canvas(self,canvas):
        self.canvas = canvas

    def set_canvascolor(self):
        canvaspc=[]
        for k in self.layers.pc:
            if len(canvaspc)==0:
                h,s,v=rgb2hsv(k[0],k[1],k[2])
                canvaspc.extend([[h,s,v]])
            else:
                h,s,v=rgb2hsv(k[0],k[1],k[2])
                hmax=0
                for n,value in enumerate(canvaspc):
                    if h<value[0]:
                        canvaspc.insert(n,[h,s,v])
                        break
                    elif n==len(canvaspc)-1:
                        canvaspc.insert(n+1,[h,s,v])
                        break
        self.canvas.pallete=canvaspc

    def hsv(self):
        for seg in self.Subsegs:
            for key in seg.pix:
                h,s,v=rgb2hsv(seg.pix[key][0],seg.pix[key][1],seg.pix[key][2])
                seg.pix[key]=[h,s,v]
        for obj in self.Segmentation.objects:
            for subseg in obj.subsegment:
                for k in subseg.pix:
                    h,s,v=rgb2hsv(subseg.pix[k][0],subseg.pix[k][1],subseg.pix[k][2])
                    subseg.pix[k]=[h,s,v]

    def paint(self):
        self.set_Subsegs()
        #self.hsv()
        time1=time.time()
        self.assigncolor()
        time2=time.time()
        print "assign_color done in ",time2-time1," s"
        self.set_canvascolor()
        im = Image.new("RGB", (400, 400), (255, 255, 255))
        for obj in self.layers.segs:
            for subseg in obj.subsegment:
                slayer=Seg_layer(subseg.edge,subseg.pix,self.canvas.canvas,im)
                slayer.render()
	'''
        for n in range(self.canvas.canvas.shape[0]):
            for p in range(self.canvas.canvas.shape[1]):
		if(self.canvas.canvas[n][p][3]<1.0):
                	print self.canvas.canvas[n][p][3]
	'''
        plt.imshow(self.canvas.canvas)
        plt.show()

if __name__ == '__main__':
    sg=Segmentation()
    sg.imread('input.jpg')
    sg.set_no(1)
    sg.set_ns(1)
    sg.segment()
    canvas=Canvas()
    canvas.set_canvas(250,250)
    canvas.set_paper('paper.jpg')
    pt=Painter(sg,canvas)
    pt.paint()























        
        

    
