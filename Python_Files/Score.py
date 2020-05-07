import math 
import numpy as np 
from skimage import draw
from skimage.io import imshow
from matplotlib import pyplot as plt


def getScore(xhit, yhit, center, region, My_Mask):
    [rows, columns] =My_Mask.board.shape

    x = int(xhit)
    y = int(yhit)

    hitAngle = math.atan2(y-center[0],x-center[1])

    hitAngle = np.mod((hitAngle * 180 / math.pi) + 360 ,360)

    for i in range(0,20):
        if (hitAngle > region[i].minAngle) and (hitAngle <= region[i].maxAngle):
            hitRegion = i
            break

    if (hitAngle > region[19].minAngle) or (hitAngle <= region[19].maxAngle):
       hitRegion = 19
    
    if (rows>=columns):
        Max=rows
    else:
        Max=columns

    x1,y1 = pol2cart(phi=region[hitRegion].minAngle,rho=Max)
    x2,y2 = pol2cart(phi=region[hitRegion].maxAngle,rho=Max)

    first_array = [center[1],x1+center[1],x2+center[1]]
    second_array = [center[0],y1+center[0],y2+center[0]]
    shape=[rows,columns]

    My_Mask.hit = poly2mask(first_array,second_array,shape)

    score = region[hitRegion].value


    if (My_Mask.single[y][x]):
        My_Mask.hit= np.multiply(My_Mask.single,My_Mask.hit)
    elif (My_Mask.double[y][x]):
        score = score * 2
        My_Mask.hit= np.multiply(My_Mask.double,My_Mask.hit)
    elif (My_Mask.triple[y][x]):
        score = score * 3
        My_Mask.hit= np.multiply(My_Mask.triple,My_Mask.hit)
    elif(My_Mask.miss[y][x]):
        score = 0 
        My_Mask.hit = My_Mask.miss
    elif(My_Mask.inner_bull[y][x]):
        score = 25
        My_Mask.hit = My_Mask.inner_bull
    elif(My_Mask.outer_bull[y][x]):
        score = 50
        My_Mask.hit = My_Mask.outer_bull
    
    
    My_Mask.hit = My_Mask.hit>0.5

    return score , My_Mask.hit



def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(np.radians(phi))
    y = rho * np.sin(np.radians(phi))
    return(x, y)



def poly2mask(vertex_row_coords, vertex_col_coords, shape):
    fill_row_coords, fill_col_coords = draw.polygon(vertex_col_coords,vertex_row_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask