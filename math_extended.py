import vector2
from math import *
from vector2 import *

def roots2(a, b, c):
    delta=b**2-4*a*c
    if delta <0:
        return (0, 0)
    else:
        return (-b+sqrt(delta))/(2*a), (-b-sqrt(delta))/(2*a)
        
def angle_of_vector2(a, b):
    temp = min(1, max(-1, (a.x*b.x+a.y*b.y)/(a.get_length()*b.get_length())))
    
    return acos(temp)
    
def nearest_zero(tulpe):
    tempmin=max(tulpe)
    for e in tulpe:
        if e > 0 and e< tempmin:
            tempmin=e
    return tempmin

def inrect(rect, point):
    difx = point[0]-rect[0][0]
    dify = point[1]-rect[0][1]
    if 0 < difx and difx < rect[1][0] and 0 < dify and dify < rect[1][1]:
        return True
    else:
        return False
