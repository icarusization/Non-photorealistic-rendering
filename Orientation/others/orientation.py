import numpy as np
from skimage import feature,io
from skimage.color import rgb2grey
import numpy.linalg as LA
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt

def neighbour(row,col,height,width):
    #row,col is the coordinate of the pixel, while height,width is the dimension of the image
    #return the coordinates of the neighboring pixels
    neighbour=[(i,j) for i in range(row-1,row+2) for j in range(col-1,col+2)]
    neighbour=filter(lambda x:x[0]>=0 and x[0]<height and x[1]>=0 and x[1]<width, neighbour)
    neighbour.remove((row,col))
    return neighbour

im=io.imread('a.jpg')
im=rgb2grey(im)
# Compute the Canny filter for two values of sigma
edges1 = feature.canny(im,sigma=2.5)
height,width=im.shape
vectors = np.ndarray((height,width,2),dtype=np.float32)
UN=np.ndarray((height,width))
VN=np.ndarray((height,width))
for i in range(height):
    for j in range(width):
        if(edges1[i][j]):
            vectors[i][j]=np.array((1.0,0.0))
        else:
            v=np.array((0.0,0.0))
            vectors[i][j]=v
        UN[i][j]=vectors[i][j][0]
        VN[i][j]=vectors[i][j][1]

Y, X = np.mgrid[0:height, 0:width]
U = -1 - np.cos(X**2 + Y)
V = 1 + X - Y
plot1 = plt.figure()
UN=np.flipud(UN)
VN=np.flipud(VN)
plt.quiver(X, Y, UN, VN,        # data
           U,                   # colour the arrows based on this array
           cmap=cm.seismic,     # colour map
           headlength=10)        # length of the arrows

plt.colorbar()                  # adds the colour bar

plt.title('Quive Plot, Dynamic Colours')
plt.show(plot1)    
