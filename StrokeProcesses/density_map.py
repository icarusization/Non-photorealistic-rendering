import numpy as np
import cv2

def get_hist(image):   
    (h,w,d) = image.shape
    hist_total = np.zeros([256,0], np.uint8)    
    for i in range(3):
        hist= cv2.calcHist([image], [i], None, [256], [0.0,255.0]) 
        res_hist = hist/(h*w)
        hist_total = np.hstack((hist_total,res_hist))
    return hist_total; 

def get_cmu(hist):
    (l,d) = hist.shape 
    cumu_hist = np.zeros(hist.shape)
    for i in range(d):
        tmp = 0
        for j in range(l):
            tmp = tmp + hist[j][i]
            cumu_hist[j][i] = tmp
    return cumu_hist

def get_match(dst,ref):
    (l,d) = dst.shape
    f_x = np.zeros(shape=dst.shape)

    for i in range(d):
        for j in range(l):
            dif_b = 1
            for k in range(l):
                dif_a = abs(dst[j][i]-ref[k][i]) 
                if(dif_a-dif_b<1.0e-08):
                    dif_b = dif_a
                    f_x[j][i] = k
                else:
                    f_x[j][i] = abs(k-1)
                    break
        if f_x[j][i]==255:
            for k in range(j,l):
                f_x[k][i]=255
            break
    return f_x


if __name__ == '__main__':
    ref_path = "./pic/2.jpg"
    dst_path = "./pic/LENA.jpg"
    out_path = "./pic/o.png"
    
    ref = cv2.imread(ref_path)
    dst = cv2.imread(dst_path)

    (h,w,d) = dst.shape

    refch = cv2.split(ref)
    dstch = cv2.split(dst)
   
    histref = get_hist(ref)   
    histdst = get_hist(dst)   
    
    cu_ref = get_cmu(histref)
    cu_dst = get_cmu(histdst)

    f_x = get_match(cu_dst,cu_ref)

    for i in range(d):
        for j in range(h):
            for k in range(w):
                pix = dstch[i][j][k]
                dstch[i][j][k] = f_x[pix][i]
    
    merge = cv2.merge(dstch)
    cv2.imshow("image",merge)
    cv2.waitKey(0)
    cv2.imwrite(out_path,dst)
    cv2.destroyAllWindows()
