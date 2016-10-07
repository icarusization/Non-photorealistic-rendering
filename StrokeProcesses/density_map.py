import numpy as np
import cv2

def calcAndDrawHist(image):   
    hist_total = np.zeros([256,0], np.uint8)    
    for i in range(3):
        hist= cv2.calcHist([image], [i], None, [256], [0.0,255.0]) 
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)    
        res_hist = hist/maxVal
        hist_total = np.hstack((hist_total,hist))
    print type(hist_total),hist_total.shape
    return hist_total; 

def calcTrans(dst,ref):
    i,j = 0,0
    print dst.shape
    table = range(256)
    for i in range(256):
        for j in range(256):
            
            if dst[i] >= ref[j-1] and dst[i] <= ref[j]:
                table[i] = j
                break
    table[255] = 255
    return table


if __name__ == '__main__':
    ref_path = "./pic/2.jpg"
    dst_path = "./pic/1.jpg"
    out_path = "./pic/o.png"
    
    ref = cv2.imread(ref_path)
    dst = cv2.imread(dst_path)
    refch = cv2.split(ref)
    dstch = cv2.split(dst)
   
    histref = calcAndDrawHist(ref)   
    histdst = calcAndDrawHist(dst)   
    print histdst.shape


    table = [calcTrans(histdst[:,i],histref[:,i]) for i in range(3)]


    print dst.shape
    print dstch[1].shape
    for i in range(3):
        for j in range(dst.shape[0]):
            for k in range(dst.shape[1]):
                pix = dstch[i][j][k]
                dstch[i][j][k] = table[i][pix]
    
    merge = cv2.merge(dstch)
    cv2.imshow("image",merge)
    cv2.waitKey(0)
    #im1 = np.zeros(dst.shape,np.uint8)
    #im2 = dst.copy()
    cv2.imwrite(out_path,dst)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


