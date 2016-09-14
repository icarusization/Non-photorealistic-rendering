import numpy as np
import pylab as plt
from skimage import feature,io
from skimage.color import rgb2grey
import lic_internal
import numpy.linalg as LA


def neighbour(row,col,height,width):
    #row,col is the coordinate of the pixel, while height,width is the dimension of the image
    #return the coordinates of the neighboring pixels
    neighbour=[(i,j) for i in range(row-1,row+2) for j in range(col-1,col+2)]
    neighbour=filter(lambda x:x[0]>=0 and x[0]<height and x[1]>=0 and x[1]<width, neighbour)
    neighbour.remove((row,col))
    return neighbour


dpi = 100
video = False
im=io.imread('a.jpg')
im=rgb2grey(im)
# Compute the Canny filter for two values of sigma
edges1 = feature.canny(im,sigma=2.5)
height,width=im.shape
vectors = np.ndarray((height,width,2),dtype=np.float32)
for i in range(height):
    for j in range(width):
        if(edges1[i][j]):
            nb=neighbour(i,j,height,width)
            if(len(nb)>=2):
                first,second=nb[0],nb[1]
                v=np.array(first)-np.array(second)
                v=v/LA.norm(v)
                vectors[i][j]=v
            else:
                v=np.array((1.0,1.0))
                vectors[i][j]=v
        else:
            v=np.array((1.0,1.0))
            vectors[i][j]=v


texture = np.random.rand(width,height).astype(np.float32)

plt.bone()
frame=0

if video:
    kernellen = 31
    for t in np.linspace(0,1,16*5):
        kernel = np.sin(np.arange(kernellen)*np.pi/kernellen)*(1+np.sin(2*np.pi*5*(np.arange(kernellen)/float(kernellen)+t)))

        kernel = kernel.astype(np.float32)

        image = lic_internal.line_integral_convolution(vectors, texture, kernel)

        plt.clf()
        plt.axis('off')
        plt.figimage(image)
        plt.gcf().set_size_inches((height/float(dpi),width/float(dpi)))
        plt.savefig("flow-%04d.png"%frame,dpi=dpi)
        frame += 1
else:
    kernellen=31
    kernel = np.sin(np.arange(kernellen)*np.pi/kernellen)
    kernel = kernel.astype(np.float32)
    image = lic_internal.line_integral_convolution(vectors, texture, kernel)

    plt.clf()
    plt.axis('off')
    plt.figimage(image)
    plt.gcf().set_size_inches((height/float(dpi),width/float(dpi)))
    plt.savefig("flow-image.png",dpi=dpi)


