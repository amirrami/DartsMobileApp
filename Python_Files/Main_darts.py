import cv2
import numpy as np 
import regions
import skimage
import skimage.measure as Ss
import math
from skimage.morphology import disk, rectangle ,binary_dilation,closing
from skimage.measure import label ,regionprops
from skimage import feature , transform
from skimage.filters import gaussian, threshold_otsu
from skimage.io import imread, imshow
from skimage.color import rgb2gray,rgb2grey
from skimage.morphology import reconstruction
from matplotlib import pyplot as plt
from alignImages import alignImages
import imutils
from Score import getScore

from skimage import data
from skimage.transform import hough_ellipse
from skimage.draw import ellipse_perimeter


def get_score(backgroundImage,dart_image):
    
    My_Mask = Mask()  #### class mask 

    ### crop images
    backgroundImage = crop_image(backgroundImage)
    dart_image = crop_image(dart_image)
    [rows, columns, channels] = backgroundImage.shape
    
    #### Create Pointmap 
      
    My_Mask= regions.findRegionMasks(backgroundImage,My_Mask)

    ### done :) 

    label_img = label(My_Mask.inner_bull)

    region = regionprops(label_img)

    max_index = get_max_index(region)
    center = region[max_index].centroid


    ##### Edge image for straight line detection
    grayBackgroundImage = rgb2gray(backgroundImage)
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
        region.maxAngle = Angles[np.mod(i+1,np.size(Angles))]
        region.value = regions_values[i]
        regions_details.append(region)

    ### align the two images using SIFT TECHNIQUE
    dart_image = alignImages(dart_image,backgroundImage)
    

    diff_image = computeDifference(cv2.cvtColor(dart_image,cv2.COLOR_RGB2GRAY),cv2.cvtColor(backgroundImage,cv2.COLOR_RGB2GRAY))
    
    ###### Difference of 2 Images 
    #blurDiff = rgb2gray(dartImageBlur-backgroundImageBlur)
    #blurDiff = blurDiff < (threshold_otsu(blurDiff)) + 0.05
    #grayDiff = rgb2gray(np.subtract(backgroundImageBlur,dartImageBlur))
    #grayDiff = grayDiff > (threshold_otsu(grayDiff)) - 0.05
    dart = np.multiply(diff_image,My_Mask.board)


    ####Find primary orientation of largest difference region
    [rows, columns, channels] = backgroundImage.shape
    dart_square = np.power(dart,2)
    SE = disk(np.round(rows/100))
    dart_square_threshed = dart_square > 0.2 * threshold_otsu(dart_square)
    My_Mask.dart = binary_dilation(dart_square_threshed,selem=SE)

    label_img = label(My_Mask.dart)
    region = regionprops(label_image=label_img)

    #get the the index of the region with max area
    max_index = get_max_index(region)

    #get the oriention in degrees
    orientation = region[max_index].orientation
    orientation = np.degrees(orientation)-90 # -90 to adjust the orientation

    #get the line structure elemet with orientation
    SE_line = strel_line(length=50,degrees=orientation)

    #close using the line to get the true shape of dart touching the board
    My_Mask.dart = closing(dart_square_threshed,selem=SE_line)

    #get the contours of the dart then detect the extrem left point which is the point the dart touch the board in
    gray_dart = skimage.img_as_ubyte(My_Mask.dart)
    cnts = cv2.findContours(gray_dart, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)
    extLeft = tuple(c[c[:, :, 0].argmin()][0])

    score ,My_Mask.hit = getScore(xhit=extLeft[0],yhit=extLeft[1],center=center,region=regions_details,My_Mask=My_Mask)

    hit_region = skimage.img_as_ubyte(My_Mask.hit)
    cnts = cv2.findContours(hit_region, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cv2.drawContours(backgroundImage, cnts, -1, (50, 255, 50), 8) 
    imshow(backgroundImage)
    plt.show()


def get_max_index(region):
    max_area = 0
    max_area_index = 0
    if len(region) > 1:
        for i in range(len(region)):
            if region[i].area > max_area:
                max_area = region[i].area
                max_area_index = i
    elif len(region) == 1:
        max_area = region[0].area
        max_area_index = 0
    return max_area_index

class Mask:
    def __init__(self):
        self.background = None
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
        self.dart = None 


class Region:
    def __init__(self):
        self.minAngle = None
        self.maxAngle = None
        self.value = None

def bresenham(x0, y0, x1, y1):
   points = []
   dx = abs(x1 - x0)
   dy = abs(y1 - y0)
   x, y = x0, y0
   sx = -1 if x0 > x1 else 1
   sy = -1 if y0 > y1 else 1
   if dx > dy:
      err = dx / 2.0
      while x != x1:
         points.append((x, y))
         err -= dy
         if err < 0:
            y += sy
            err += dx
         x += sx
   else:
      err = dy / 2.0
      while y != y1:
         points.append((x, y))
         err -= dx
         if err < 0:
            x += sx
            err += dy
         y += sy
   points.append((x, y))

   return points


def strel_line(length, degrees):
   if length >= 1:
      theta = degrees * np.pi / 180
      x = round((length - 1) / 2 * np.cos(theta))
      y = -round((length - 1) / 2 * np.sin(theta))
      points = bresenham(-x, -y, x, y)
      points_x = [point[0] for point in points]
      points_y = [point[1] for point in points]
      n_rows = int(2 * max([abs(point_y) for point_y in points_y]) + 1)
      n_columns = int(2 * max([abs(point_x) for point_x in points_x]) + 1)
      strel = np.zeros((n_rows, n_columns))
      rows = ([point_y + max([abs(point_y) for point_y in points_y]) for point_y in points_y])
      columns = ([point_x + max([abs(point_x) for point_x in points_x]) for point_x in points_x])
      idx = []
      for x in zip(rows, columns):
         idx.append(np.ravel_multi_index((int(x[0]), int(x[1])), (n_rows, n_columns)))
      strel.reshape(-1)[idx] = 1

   return strel





def computeDifference(grey1,grey2):
    # blur
    grey2 = cv2.blur(grey2,(5,5))
    grey1 = cv2.blur(grey1,(5,5))
    #normalize
    grey1 = cv2.equalizeHist(grey1)
    grey2 = cv2.equalizeHist(grey2)
    clahe = cv2.createCLAHE(clipLimit=5,tileGridSize=(10,10))
    #clahe
    grey1 = clahe.apply(grey1)
    grey2 = clahe.apply(grey2)
    #diff
    diff = cv2.subtract(grey2,grey1) + cv2.subtract(grey1,grey2)
    dif_thred = diff > threshold_otsu(diff)
    dif_thred = skimage.img_as_ubyte(dif_thred)    
    return dif_thred


def crop_image(image):
    gray_image = rgb2gray(image)
    blur_image = gaussian(gray_image,5)
    BWImage = blur_image > threshold_otsu(blur_image)

    ### image fill
    seed = np.copy(~BWImage)
    seed[1:-1, 1:-1] = (~BWImage).max()
    mask = ~BWImage
    background = reconstruction(seed, mask, method='erosion')

    ## cropping image
    label_img = label(background)
    region = regionprops(label_img)

    max_index = get_max_index(region)

    x1 = region[max_index].bbox[1] # min_col
    x2 = region[max_index].bbox[3] # max_col
    y1 = region[max_index].bbox[0] # min_row
    y2 = region[max_index].bbox[2] # max_row

    image = image[y1:y2,x1:x2]

    return image

board_img =imread("dartBoard2.jpg")

dart_img =imread("dart12.jpg")   

get_score(board_img,dart_img)



