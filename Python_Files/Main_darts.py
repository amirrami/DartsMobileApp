import cv2
import numpy as np 
import regions
import skimage
import skimage.measure as Ss
import math

#import props

from skimage.measure import label ,regionprops


from skimage import feature , transform

import skimage.measure as SS 
from skimage.filters import gaussian, threshold_otsu
from skimage.io import imread, imshow
from skimage.color import rgb2gray

from skimage.morphology import reconstruction
from matplotlib import pyplot as plt


def get_score(base_image,dart_image):
    
    My_Mask = Mask()  #### class mask 

    backgroundImage = skimage.img_as_float64(base_image)
    dartImage= skimage.img_as_float64(dart_image)

    grayBackgroundImage = rgb2gray(backgroundImage)

    BWBackgroundImage = grayBackgroundImage > threshold_otsu(grayBackgroundImage)


    ### imfill done :) 
    seed = np.copy(~BWBackgroundImage)
    seed[1:-1, 1:-1] = ~BWBackgroundImage.max()
    mask = ~BWBackgroundImage

    My_Mask.background = reconstruction(seed, mask, method='dilation')

    
    ##### cancel cropping to both images 
    #S = SS.regionprops_table(temp, properties = ['bbox','area'])
    
    grayDartImage = rgb2gray(dartImage)

    [rows, columns, channels] = backgroundImage.shape
    

    #### Create Pointmap 

    My_Mask= regions.findRegionMasks(backgroundImage,My_Mask)

    ### done :) 

    label_img = label(My_Mask.inner_bull)

    region = regionprops(label_img)

    center = region[0].centroid


    ##### Edge image for straight line detection
    temp_image = grayBackgroundImage * My_Mask.board 

    edgeImage = feature.canny(temp_image,high_threshold=0.4,low_threshold=0.2)

    tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 3600)
    [H,theta,rho] = transform.hough_line(edgeImage,theta=tested_angles)

    thresh = np.amax(H)
    thresh = np.ceil(thresh*0.05)
    
    #####  Detect Peaks
    hspace, angle, dists = transform.hough_line_peaks(H,theta,rho,num_peaks=10,threshold=thresh)


    ##### change angles theta to degrees 
    theta_degree= np.degrees(angle)

    angles = []
    angles_180 =[]
    for a in theta_degree:
        angles.append(a-90+360)
        angles_180.append(a+90+360)
    
    ######  angles - Zero degrees = up 
    Angles = np.concatenate((angles,angles_180),axis=0)
    Angles = np.mod(Angles,360)
    Angles = np.sort(Angles)


    ##### Draw lines detected
    """ for i in range(len(dists)): 
        
        theta = angle[i]
        r = dists[i]
        # Stores the value of cos(theta) in a 
        a = np.cos(theta) 
    
        # Stores the value of sin(theta) in b 
        b = np.sin(theta) 
        
        # x0 stores the value rcos(theta) 
        x0 = a*r 
        
        # y0 stores the value rsin(theta) 
        y0 = b*r 
        
        # x1 stores the rounded off value of (rcos(theta)-1000sin(theta)) 
        x1 = int(x0 + 1000*(-b)) 
        
        # y1 stores the rounded off value of (rsin(theta)+1000cos(theta)) 
        y1 = int(y0 + 1000*(a)) 
    
        # x2 stores the rounded off value of (rcos(theta)+1000sin(theta)) 
        x2 = int(x0 - 1000*(-b)) 
        
        # y2 stores the rounded off value of (rsin(theta)-1000cos(theta)) 
        y2 = int(y0 - 1000*(a)) 
        
        # cv2.line draws a line in img from the point(x1,y1) to (x2,y2). 
        # (0,0,255) denotes the colour of the line to be  
        #drawn. In this case, it is red.  
        cv2.line(backgroundImage,(x1,y1), (x2,y2), (0,0,255),2) 

    imshow(backgroundImage)
    plt.show() """


    ### construct the 20 region of the dart board
    regions_values = [10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13, 6]
    regions_details = []
    for i in range(len(regions_values)):
        region = Region()
        region.minAngle = Angles[i]
        region.maxAngle = Angles[np.mod(i,np.size(angles))+1]
        region.value = regions_values[i]
        regions_details.append(region)

    





def image_fill (gray):
    des = cv2.bitwise_not(gray)
    contour,hier = cv2.findContours(des,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contour:
        cv2.drawContours(des,[cnt],0,255,-1)

    gray = cv2.bitwise_not(des)
    return gray 



class Mask:
    def __init__(self):
        self.background=None 
        self.red = None 
        self.green = None 
        self.multipliers=None 
        self.multRings=None 
        self.board=None 
        self.miss=None 
        self.single=None
        self.double=None
        self.trible=None 
        self.inner_bull=None 
        self.outer_bull=None 

class Region:
    def __init__(self):
        self.minAngle = None
        self.maxAngle = None
        self.value = None






board_img =imread("dartBoard.jpg")

dart_img =imread("dart18.jpg")   

get_score(board_img,dart_img)

