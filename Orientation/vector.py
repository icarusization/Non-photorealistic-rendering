import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pylab import *


def direction_array(im):
    im = Image.open('boundary.jpg')

    w, h = im.size

    print w, h
    im = im.convert("L")
    data = im.getdata()

    data = np.array(data)

    data = np.reshape(data, (w, h))

    '''
    n=8
    X,Y=np.mgrid[0:w,0:h]
    quiver(X,Y,1,1)
    show()
    '''
    x = np.arange(0, w, 1)
    y = np.arange(0, -h, -1)

    u = zeros([w, h])
    v = zeros([w, h])
    [X, Y] = meshgrid(x, y)

    # plt.axis([0,5,-5,0])

    PI = 3.1415926
    f = {}

    for r in range(h):
        for c in range(w):
            f[(c, -r)] = [0, 0]

    # hold

    for r in range(h):
        for c in range(w):
            if data[c][r] != 0:
                if c - 1 >= 0 and c + 1 < w and r - 1 >= 0 and r + 1 < h:
                    direction = 0
                    if data[c + 1][r + 1] != 0:
                        direction = direction + 1
                    if data[c + 1][r - 1] != 0:
                        direction = direction + 1
                    if data[c - 1][r - 1] != 0:
                        direction = direction + 1
                    if data[c - 1][r + 1] != 0:
                        direction = direction + 1
                    if direction == 0:
                        if data[c + 1][r] != 0:
                            f[(c, r)] = [1, 0]
                            u[c][r] = 1
                            v[c][r] = 0
                        elif data[c][r + 1] != 0:
                            f[(c, r)] = [1, 3 * PI / 2]
                            u[c][r] = 0
                            v[c][r] = -1
                        elif data[c - 1][r] != 0:
                            f[(c, r)] = [1, PI]
                            u[c][r] = -1
                            v[c][r] = 0

                        elif data[c][r - 1] != 0:
                            f[(c, r)] = [1, PI / 2]
                            u[c][r] = 0
                            v[c][r] = 1
                        # else:

                    elif direction == 1:
                        if data[c + 1][r - 1] != 0:
                            f[(c, r)] = [1, PI / 4]
                            u[c][r] = 1
                            v[c][r] = 1

                        elif data[c + 1][r + 1] != 0:
                            f[(c, r)] = [1, 7 * PI / 4]
                            u[c][r] = 1
                            v[c][r] = -1

                        elif data[c - 1][r + 1] != 0:
                            f[(c, r)] = [1, 5 * PI / 4]
                            u[c][r] = -1
                            v[c][r] = -1

                        elif data[c - 1][r - 1] != 0:
                            f[(c, r)] = [1, 3 * PI / 4]
                            u[c][r] = -1
                            v[c][r] = 1
                            # else:
                    elif direction == 2:
                        if data[c + 1][r - 1] != 0 and data[c + 1][r + 1] != 0:
                            f[(c, r)] = [1, 0]
                            u[c][r] = 1
                            v[c][r] = 0

                        elif data[c + 1][r + 1] != 0 and data[c - 1][r + 1] != 0:
                            f[(c, r)] = [1, 3 * PI / 2]
                            u[c][r] = 0
                            v[c][r] = -1

                        elif data[c - 1][r + 1] != 0 and data[c - 1][r - 1] != 0:
                            f[(c, r)] = [1, PI]
                            u[c][r] = -1
                            v[c][r] = 0

                        elif data[c - 1][r - 1] != 0 and data[c + 1][r - 1] != 0:
                            f[(c, r)] = [1, PI / 2]
                            u[c][r] = 0
                            v[c][r] = 1

                            # else:
                    elif direction == 3:
                        if data[c + 1][r - 1] != 0 and data[c + 1][r + 1] != 0 and data[c - 1][r + 1] != 0:
                            f[(c, r)] = [1, 7 * PI / 4]
                            u[c][r] = 1
                            v[c][r] = -1

                        elif data[c + 1][r + 1] != 0 and data[c - 1][r + 1] != 0 and data[c - 1][r - 1] != 0:
                            f[(c, r)] = [1, 5 * PI / 4]
                            u[c][r] = -1
                            v[c][r] = -1

                        elif data[c - 1][r + 1] != 0 and data[c - 1][r - 1] != 0 and data[c + 1][r - 1] != 0:
                            f[(c, r)] = [1, 3 * PI / 4]
                            u[c][r] = -1
                            v[c][r] = 1

                        elif data[c - 1][r - 1] != 0 and data[c + 1][r - 1] != 0 and data[c + 1][r + 1] != 0:
                            f[(c, r)] = [1, PI / 4]
                            u[c][r] = 1
                            v[c][r] = 1

                        else:
                            f[(c, r)] = [1, 0]
                            u[c][r] = 1
                            v[c][r] = 0
                else:
                    f[(c, r)] = [0, 0]
                    u[c][r] = 0
                    v[c][r] = 0
            else:
                f[(c, r)] = [0, 0]
                u[c][r] = 0
                v[c][r] = 0

    for r in range(h):
        for c in range(w):
            if not f.has_key((c, r)):
                f[(c, r)] = [0, 0]
    return f


