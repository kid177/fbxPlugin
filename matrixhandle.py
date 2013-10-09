# -*- coding:gbk -*-
from math import cos, sin, asin, degrees, sqrt, pi
"""
cz*cy + sx*cy*sz      sz*cx              -sy*cz + sz*sx*cy
-sz*cy + cz*sx*sy     cz*cx              sy*sz+sx*cy*cz
    cx*sy              -sx                  cx*cy

"""
def check(h, p, r, matrix):
    eps = 0
    if matrix[0][0] * (cos(r) * cos(p) + sin(h) * sin(p) * sin(r)) < eps:
        return False
    if matrix[0][1] * (cos(h) * sin(r)) < eps:
        return False
    if matrix[0][2] * (-sin(p) * cos(r) + sin(r) * sin(h) * cos(p)) < eps:
        return False
    if matrix[1][0] * (-sin(r) * cos(p) + cos(r) * sin(h) * sin(p)) < eps:
        return False
    if matrix[1][1] * (cos(r) * cos(h)) < eps:
        return False
    if matrix[1][2] * (sin(p) * sin(r) + sin(h) * cos(p) * cos(r)) < eps:
        return False
    if matrix[2][0] * (cos(h) * sin(p)) < eps:
        return False
    if matrix[2][1] * (-sin(h)) < eps:
        return False
    if matrix[2][2] * (cos(h) * cos(p)) < eps:
        return False
    return True

def GetScalingFromMatrix(matrix):
    temp = []
    for i in xrange(0, 3):
        tt = 0
        for j in xrange(0, 3):
            tt += matrix[i][j] * matrix[i][j]
        temp.append(sqrt(tt))
        for j in xrange(0, 3):
            matrix[i][j] /= temp[i]
    return temp

def GetRotaionFromMatirx(matrix):

    
    h = asin(-matrix[2][1])
    h1 = degrees(h)
    
    temp = matrix[2][0] / cos(h)
    if temp < -1:
        temp = -1
    if temp > 1:
        temp = 1
    p = asin(temp)
    p1 = degrees(p)
    
    temp = matrix[0][1] / cos(h)
    if temp < -1:
        temp = -1
    if temp > 1:
        temp = 1
    r = asin(temp)
    r1 = degrees(r)

    for i in xrange(0, 8):
        temph = h
        tempp = p
        tempr = r
        if i & 1:
            temph = pi - temph
        if i >> 1 & 1:
            tempp = pi - tempp
        if i >> 2 & 1:
            tempr = pi - tempr
        if check(temph, tempp, tempr, matrix):
            h1 = degrees(temph)
            p1 = degrees(tempp)
            r1 = degrees(tempr)
            break
    return (-h1, -p1, r1)
