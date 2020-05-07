import cv2
import numpy as np 
import skimage
from skimage.measure import label ,regionprops
from skimage.filters import gaussian, threshold_otsu
from skimage.io import imshow
from skimage.color import rgb2gray
from skimage.morphology import reconstruction
from matplotlib import pyplot as plt
from skimage import draw



MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15


def alignImages(im1, im2):

    # Convert images to grayscale
    im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    
    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
    
    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)
    
    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    #cv2.imwrite("matches.jpg", imMatches)
    
    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt
    
    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))
    
    return im1Reg



  

def  crop_image(image):
    gray_image = rgb2gray(image)
    blur_image = gaussian(gray_image,5)
    BWImage = blur_image > threshold_otsu(blur_image)

    ### image fill
    seed = np.copy(~BWImage)
    seed[1:-1, 1:-1] = (~BWImage).max()
    mask = ~BWImage
    background = reconstruction(seed, mask, method='erosion')

    ### get bounding box
    label_img = label(background)
    region = regionprops(label_img)
    max_index = get_max_index(region)

    ## cropping image
    x1 = region[max_index].bbox[1] # min_col
    x2 = region[max_index].bbox[3] # max_col
    y1 = region[max_index].bbox[0] # min_row
    y2 = region[max_index].bbox[2] # max_row
    image = image[y1:y2,x1:x2]

    return image


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


def Draw_lines_detected(angle,dists,backgroundImage):
        for i in range(len(dists)): 
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
        plt.show() 


### chnage x and y from cartizian plane to polar plane
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

### chnage x and y from polar plane to cartizian plane
def pol2cart(rho, phi):
    x = rho * np.cos(np.radians(phi))
    y = rho * np.sin(np.radians(phi))
    return(x, y)


def poly2mask(vertex_row_coords, vertex_col_coords, shape):
    fill_row_coords, fill_col_coords = draw.polygon(vertex_col_coords,vertex_row_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask
