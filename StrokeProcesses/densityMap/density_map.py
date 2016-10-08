import numpy as np
import cv2
import math as m


def get_hist(image):  
    if len(image.shape)==3:
        (h,w,d) = dst.shape
    else:
        (h,w),d = dst.shape,1
    hist_total = np.zeros([256,0], np.uint8)    
    for i in range(d):
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

def get_exp_match(dst,cu_dst):
    (l,d) = cu_dst.shape
    cu_exp = np.zeros(shape=cu_dst.shape)
    for i in range(d):
        for j in range(l):
            lamda = 3*np.mean(dst)
            cu_exp[j][i] = exp_cdf(j,lamda)
    print cu_dst.shape,cu_ref.shape
    f_x = get_match(cu_dst,cu_exp) 
    return f_x

def exp_cdf(x,lamda):
    return 1-m.exp(-lamda*x)

if __name__ == '__main__':
    ref_path = "./pic/output.png"
    #dst_path = "./pic/LENA.jpg"
    dst_path = "./pic/s.png"
    out_path = "./pic/mix_out.png"
    
    ref = cv2.imread(ref_path,0)
    dst = cv2.imread(dst_path,0)

    if len(dst.shape)==3:
        (h,w,d) = dst.shape
    else:
        (h,w),d = dst.shape,1

    refch = cv2.split(ref)
    dstch = cv2.split(dst)
   
    histref = get_hist(ref)   
    histdst = get_hist(dst)   
    
    cu_ref = get_cmu(histref)
    cu_dst = get_cmu(histdst)

    f_x = get_match(cu_dst,cu_ref)
    #f_x = get_exp_match(histdst,cu_dst)

    for i in range(d):
        for j in range(h):
            for k in range(w):
                pix = dstch[i][j][k]
                dstch[i][j][k] = f_x[pix][i]
    
    merge = cv2.merge(dstch)
    #cv2.imshow("dst",dst)
    #cv2.imshow("ref",ref)
    #cv2.imshow("image",merge)
    #cv2.waitKey(0)
    cv2.imwrite(out_path,merge)
    cv2.destroyAllWindows()
