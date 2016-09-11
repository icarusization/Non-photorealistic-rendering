import random

length = 100
width = 100


def transfer_data(f, r, dic):
    for i in range(length):
        for j in range(width):
            l = []
            if f[(i, j)][0] == 1:
                l.append(f[(i, j)][1])
                l.append(float(1.0))
                dic[(i, j)] = l                    # For line point it has weight 1.0
            else:
                l.append(r[(i, j)])
                l.append(float(0.01))
                dic[(i, j)] = l                    # For noise point it has weight 0.0 to be affected by outline
    return dic


def iteration(n, dic):
    for k in range(n):
        for i in range(length):
            for j in range(width):
                point = dic[(i, j)]
                if point[1] != 1.0:
                    point = square_central(dic, i, j)
                    #point[1] = 2*point[1]/(1+point[1])
                    dic[(i, j)] = point
    return dic


def square_central(dic, i, j):
    angle_list = []
    weight_list = []
    angle = 0
    weight = 0

    for m in [i-1, i, i+1]:
        for n in [j-1, j, j+1]:
            if m>=0 and m<length and n>=0 and n<width and (m!=i or n!=j):
                point = dic[(m, n)]
                angle_list.append(point[0])
                weight_list.append(point[1])

    weight_sum = sum(weight_list)
    if weight_sum != 0:
        for i in range(len(angle_list)):
            angle += angle_list[i]*weight_list[i]
        angle = angle / weight_sum                          # Calculate the relative weight for neighbour points
        angle += random.random()*3.14/80                    # Add a noise on angle to avoid parallel

    l = len(weight_list)
    for i in range(l):
        weight += weight_list[i]/l

    return [angle, weight]


