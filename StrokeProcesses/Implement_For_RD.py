# Implementation for ReactionDiffusion.
import math

def get_value(reaction):
    eff = []
    for properties in reaction:
        eff.append(properties)
    return eff


def pass_threshold(eff, ratio, mode):
    pass


def iteration(n, eff, dif, neighbour):

    for k in range(n):
        for i in range(len(eff)):
            neigh_list = neighbour[i]
            l = len(neigh_list)
            eff[i] *= (1-l)*dif+l
            for p in neigh_list:
                eff[i] += eff[p]*dif

            if k % 5 == 0:
                eff[i] *= 1.02  # (1+random.random()*0.5)
            eff[i] /= (l + 1)

    return eff


def iteration_color(n, color_eff, dif, neighbour):
    eff = []
    for ele in color_eff:
        eff.append(math.sqrt(ele[1]))

    small, big = dif*dif, math.sqrt(dif)
    for k in range(n):
        for i in range(len(eff)):
            neigh_list = neighbour[i]
            l = len(neigh_list)
            if eff[i]<0.5:
                dif = big
            else:
                dif = small
            eff[i] *= (1 - l) * dif + l
            for p in neigh_list:
                eff[i] += eff[p] * dif

            if k % 5 == 0:
                eff[i] *= 1.02  # (1+random.random()*0.5)
            eff[i] /= (l + 1)

    for i in range(len(color_eff)):
        color_eff[i][1] = eff[i]
    return color_eff
