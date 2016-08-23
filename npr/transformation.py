#-*- coding:utf-8 -*-
import numpy as np
#from Utility import *
from skimage import io
from skimage.transform import rotate
from skimage.transform import rescale
import matplotlib.pyplot as plt
'''
先读了一张图片，当做一个segment来测试
'''
im=io.imread('input.jpg')
height=im.shape[0]
width=im.shape[1]
out=np.ndarray(shape=5)
i=0
for row in range(height):
    for col in range(width):
        pix=np.ndarray(shape=5, dtype = int)
        pix[0:3]=im[row][col]
        pix[3:5]=[col,row]
        if not(pix[0]>=245 and pix[1]>=245 and pix[2]>=245):
            i=i+1
            if i==1:
                out={(col,row):pix[0:3]}
            else:
                out[(col,row)]=pix[0:3]

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
'''
print 功能：
输入out是像素点（5维）的list
如果canvas=None, 就用最小的框框定并显示所有像素点
如果canvas=[x,y],就会在[x,y]的范围内显示所有像素点。注意：像素点不能超出x,y的范围，否则会报错。None则没有这个问题
'''
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
            result[row][col][0]=255#这三个是画布底色，可调
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
    plt.imshow(result)
    plt.show()
'''
输入out是像素点（5维）的list
shift就是平移，x是向x轴正方形移动的像素格数，y是向y轴正方向，某一方向不移就写0。注意：移动时小心移出canvas范围
'''
def shift(out,x,y):
    i=0
    for k in out:
        i=i+1
        col=k[0]+x
        row=k[1]+y
        pix=out[k]
        if i==1:
            rout={(col,row):pix}
        else:
            rout[(col,row)]=pix
    return rout	
'''
输入out是像素点（5维）的list
degree 是逆时针转动角度
centre不写时默认为几何中心，写的话就是centre=(x,y)，centre就是转动中心。同样注意不要转出画布范围
'''
def rotation(out,degree,centre=None):
    z=0
    height,width,xmin,ymin=findscale(out)
    result=np.empty((height,width,3))
    for row in range(height):
        for col in range(width):
            result[row][col][0]=255
            result[row][col][1]=255
            result[row][col][2]=255
    
    z =0
    
    for key in out:
        x=key[0]-xmin
        y=key[1]-ymin
        result[y][x]=[out[key][0],out[key][1],out[key][2]]
    result=np.uint8(result)
    if centre==None:
        result=rotate(result,degree,order=4,resize=True)
    else:
        result=rotate(result,degree,center=centre,order=4,resize=True)
    result=result*255
    result=np.uint8(result)
    rout=np.ndarray(shape=5)
    i=0
    height=result.shape[0]
    width=result.shape[1]
    for row in range(height):
        for col in range(width):
            pix=np.ndarray(shape=5, dtype = int)
            pix[0:3]=result[row][col]
            pix[3:5]=[col,row]
            if not((pix[0]>=250 and pix[1]>=250 and pix[2]>=250)or(pix[0]<=5 and pix[1]<=5 and pix[1]<=5)):
                i=i+1
                if i==1:
                    rout={(col,row):pix[0:3]}
                else:
                    rout[(col,row)]=pix[0:3]

    return rout
'''
输入out是像素点（5维）的list
n是缩放比率，比如0.8，比如1.3
缩放以几何中心为基准
'''

def rescaling(out,n):
    z=0
    oheight,owidth,xmin,ymin=findscale(out)
    result=np.empty((oheight,owidth,3))
    for row in range(oheight):
        for col in range(owidth):
            result[row][col][0]=255
            result[row][col][1]=255
            result[row][col][2]=255
    
    z =0
    
    for k in out:
        x=k[0]-xmin
        y=k[1]-ymin
        result[y][x]=[out[k][0],out[k][1],out[k][2]]
    result=np.uint8(result)
    result=rescale(result,n,order=4)
    result=result*255
    
    result=np.uint8(result)
    rout=np.ndarray(shape=5)
    i=0
    height=result.shape[0]
    width=result.shape[1]
    row=0
    col=0
    for row in range(height):
        for col in range(width):
            
            pix=np.ndarray(shape=5, dtype = int)
            pix[0:3]=result[row][col]
            pix[3:5]=[col+xmin,row+ymin]
            
            if not((pix[0]>=250 and pix[1]>=250 and pix[2]>=250)or(pix[0]<=5 and pix[1]<=5 and pix[1]<=5)):
               
                i=i+1
                if i==1:
                    rout={(col+xmin,row+ymin):pix[0:3]}
                else:
                    rout[(col+xmin,row+ymin)]=pix[0:3]
                    
    xs=int((1-n)/2*owidth)
    ys=int((1-n)/2*oheight)
    rout=shift(rout,xs,ys)
    return rout
    

    

if __name__=="__main__":
    segprint(out,canvas=[500,500])
    a=rotation(out,60)
    a=shift(a,100,100)
    segprint(a,canvas=[500,500])
