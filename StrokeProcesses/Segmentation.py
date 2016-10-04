#!/usr/bin/env python
'''
https://github.com/abidrahmank
===============================================================================
Interactive Image Segmentation using GrabCut algorithm.
This sample shows interactive image segmentation using grabcut algorithm.
USAGE :
    python grabcut.py <filename>
README FIRST:
    Two windows will show up, one for input and one for output.

    At first, in input window, draw a rectangle around the object using
mouse right button. Then press 'n' to segment the object (once or a few times)
For any finer touch-ups, you can press any of the keys below and draw lines on
the areas you want. Then again press 'n' for updating the output.
Key '0' - To select areas of sure background
Key '1' - To select areas of sure foreground
Key '2' - To select areas of probable background
Key '3' - To select areas of probable foreground
Key 'n' - To update the segmentation
Key 'r' - To reset the setup
Key 's' - To save the results
===============================================================================
'''

import numpy as np
import cv2
import sys

class Segmentation:
    def __init__(self):
        self.BLUE = [255,0,0]        # rectangle color
        self.RED = [0,0,255]         # PR BG
        self.GREEN = [0,255,0]       # PR FG
        self.BLACK = [0,0,0]         # sure BG
        self.WHITE = [255,255,255]   # sure FG

        self.DRAW_BG = {'color' : self.BLACK, 'val' : 0}
        self.DRAW_FG = {'color' : self.WHITE, 'val' : 1}
        self.DRAW_PR_FG = {'color' : self.GREEN, 'val' : 3}
        self.DRAW_PR_BG = {'color' : self.RED, 'val' : 2}

        # setting up flags
        self.rect = (0,0,1,1)
        self.drawing = False         # flag for drawing curves
        self.rectangle = False       # flag for drawing rect
        self.rect_over = False       # flag to check if rect drawn
        self.rect_or_mask = 100      # flag for selecting rect or mask mode
        self.value = self.DRAW_FG         # drawing initialized to FG
        self.thickness = 3           # brush thickness

        #global values
        self.img=None
        self.img2=None
        self.mask=None
        self.ix=None
        self.iy=None

    def read_image(self,filename):
        self.img = cv2.imread(filename)
        self.img2 = self.img.copy()                               # a copy of original image
        self.mask = np.zeros(self.img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG

    def onmouse(self,event,x,y,flags,param):

        # Draw Rectangle
        if event == cv2.EVENT_RBUTTONDOWN:
            self.rectangle = True
            self.ix,self.iy = x,y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.rectangle == True:
                self.img = self.img2.copy()
                cv2.rectangle(self.img,(self.ix,self.iy),(x,y),self.BLUE,2)
                self.rect = (self.ix,self.iy,abs(self.ix-x),abs(self.iy-y))
                self.rect_or_mask = 0

        elif event == cv2.EVENT_RBUTTONUP:
            self.rectangle = False
            self.rect_over = True
            cv2.rectangle(self.img,(self.ix,self.iy),(x,y),self.BLUE,2)
            self.rect = (self.ix,self.iy,abs(self.ix-x),abs(self.iy-y))
            self.rect_or_mask = 0
            print " Now press the key 'n' a few times until no further change \n"

        # draw touchup curves

        if event == cv2.EVENT_LBUTTONDOWN:
            if self.rect_over == False:
                print "first draw rectangle \n"
            else:
                self.drawing = True
                cv2.circle(self.img,(x,y),self.thickness,self.value['color'],-1)
                cv2.circle(self.mask,(x,y),self.thickness,self.value['val'],-1)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv2.circle(self.img,(x,y),self.thickness,self.value['color'],-1)
                cv2.circle(self.mask,(x,y),self.thickness,self.value['val'],-1)

        elif event == cv2.EVENT_LBUTTONUP:
            if self.drawing == True:
                self.drawing = False
                cv2.circle(self.img,(x,y),self.thickness,self.value['color'],-1)
                cv2.circle(self.mask,(x,y),self.thickness,self.value['val'],-1)

    def segment(self):
        # print documentation
        print __doc__
        print " Instructions : \n"
        print " Draw a rectangle around the object using right mouse button \n"


        output = np.zeros(self.img.shape,np.uint8)           # output image to be shown

        # input and output windows
        cv2.namedWindow('output')
        cv2.namedWindow('input')
        cv2.setMouseCallback('input',self.onmouse)
        cv2.moveWindow('input',self.img.shape[1]+10,90)

        while(1):

            cv2.imshow('output',output)
            cv2.imshow('input',self.img)
            k = cv2.waitKey(1)

            # key bindings
            if k == 27:         # esc to exit
                break
            elif k == ord('0'): # BG drawing
                print " mark background regions with left mouse button \n"
                self.value = self.DRAW_BG
            elif k == ord('1'): # FG drawing
                print " mark foreground regions with left mouse button \n"
                self.value = self.DRAW_FG
            elif k == ord('2'): # PR_BG drawing
                self.value = self.DRAW_PR_BG
            elif k == ord('3'): # PR_FG drawing
                self.value = self.DRAW_PR_FG
            elif k == ord('s'):
                #bar = np.zeros((img.shape[0],5,3),np.uint8)
                #res = np.hstack((img2,bar,img,bar,output))
                cv2.imwrite('output.png',output)
                print " Result saved as image \n"
            elif k == ord('r'): # reset everything
                print "resetting \n"
                self.rect = (0,0,1,1)
                self.drawing = False
                self.rectangle = False
                self.rect_or_mask = 100
                self.rect_over = False
                self.value = self.DRAW_FG
                self.img = self.img2.copy()
                self.mask = np.zeros(self.img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
                self.output = np.zeros(self.img.shape,np.uint8)           # output image to be shown
            elif k == ord('n'): # segment the image
                print """ For finer touchups, mark foreground and background after pressing keys 0-3
                    and again press 'n' \n"""
                if (self.rect_or_mask == 0):         # grabcut with rect
                    bgdmodel = np.zeros((1,65),np.float64)
                    fgdmodel = np.zeros((1,65),np.float64)
                    cv2.grabCut(self.img2,self.mask,self.rect,bgdmodel,fgdmodel,1,cv2.GC_INIT_WITH_RECT)
                    self.rect_or_mask = 1
                elif self.rect_or_mask == 1:         # grabcut with mask
                    bgdmodel = np.zeros((1,65),np.float64)
                    fgdmodel = np.zeros((1,65),np.float64)
                    cv2.grabCut(self.img2,self.mask,self.rect,bgdmodel,fgdmodel,1,cv2.GC_INIT_WITH_MASK)

            mask2 = np.where((self.mask==1) + (self.mask==3),255,0).astype('uint8')
            output = cv2.bitwise_and(self.img2,self.img2,mask=mask2)

        cv2.destroyAllWindows()

if __name__=="__main__":
    Sg=Segmentation()
    Sg.read_image("123.png")
    Sg.segment()