import cv2
import numpy as np 
import skimage.measure as SS 
from skimage.filters import gaussian, threshold_otsu
from skimage.io import imread,imshow
from skimage.color import rgb2gray
import skimage
from skimage.morphology import disk
from skimage.morphology import binary_closing
from skimage.morphology import reconstruction
from matplotlib import pyplot as plt

def findRegionMasks(image,My_Mask):
    grayImage = rgb2gray(image)

    image = skimage.img_as_float64(image)
    redRegions = image[:,:,0]-grayImage
    My_Mask.red = redRegions > threshold_otsu(redRegions) -0.05

    greenRegions = image[:,:,1]-grayImage
    My_Mask.green = greenRegions > (-threshold_otsu(greenRegions)) - 0.05

    My_Mask.multipliers=My_Mask.red + My_Mask.green

    My_Mask.multipliers = skimage.img_as_float64(My_Mask.multipliers)


    SE = disk(np.round(np.size(image[:,1,1])/100))
    
    My_Mask.multRings = binary_closing(My_Mask.multipliers,SE)

    My_Mask.multRings = skimage.img_as_float64(My_Mask.multRings)

    ### imfill holes of multrings  
    seed = np.copy(My_Mask.multRings)
    seed[1:-1, 1:-1] = My_Mask.multRings.max()
    mask = My_Mask.multRings
    My_Mask.board = reconstruction(seed, mask, method='erosion')

    change_to_bool = np.array(My_Mask.board , dtype=bool)

    My_Mask.miss= ~change_to_bool

    My_Mask.single = My_Mask.board-My_Mask.multRings


    #### imfill holes of My_mask.single 

    seed = np.copy(My_Mask.single)
    seed[1:-1, 1:-1] = My_Mask.single.max()
    mask = My_Mask.single

    Tempp= reconstruction(seed, mask, method='erosion')

    My_Mask.double = My_Mask.board-Tempp


    ### inner Ring 
    inner_Ring  = My_Mask.board-My_Mask.double-My_Mask.single

    seed = np.copy(inner_Ring)
    seed[1:-1, 1:-1] = inner_Ring.max()
    mask = inner_Ring

    Tempp= reconstruction(seed, mask, method='erosion')


    inner_Ring = Tempp-inner_Ring


    ### triple region 
    seed = np.copy(inner_Ring)
    seed[1:-1, 1:-1] = inner_Ring.max()
    mask = inner_Ring

    Tempp= reconstruction(seed, mask, method='erosion')

    My_Mask.triple = My_Mask.board-My_Mask.double-My_Mask.single - Tempp

    My_Mask.triple[My_Mask.triple < 0] = 0


    ### outer Bull 
    My_Mask.outer_bull = (My_Mask.multRings - My_Mask.double - My_Mask.triple) * My_Mask.green
       
    #### inner Bull 

    My_Mask.inner_bull = (My_Mask.multRings - My_Mask.double - My_Mask.triple) * My_Mask.red


    return My_Mask 










