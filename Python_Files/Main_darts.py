import cv2
import numpy as np 
import math
import skimage
from skimage.morphology import disk ,binary_dilation,binary_closing,closing
from skimage.measure import label ,regionprops
from skimage import feature , transform
from skimage.filters import gaussian, threshold_otsu
from skimage.io import imread, imshow
from skimage.color import rgb2gray
from skimage.morphology import reconstruction
from matplotlib import pyplot as plt
import imutils
import utils



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


class Dart_Detection():
    def __init__(self,boardImage):
        self.boardImage = boardImage
        self.dartImage = None
        self.myMask = Mask()
        self.dartScore = None
        self.boardImage = utils.crop_image(self.boardImage)
        self.outputBoardImage = self.boardImage


    def computeScore(self,dart_image):    
        
        self.dartImage = dart_image

        ### crop dart image
        self.dartImage = utils.crop_image(self.dartImage)
        
        #### Create Pointmap that contain all regions of the dart board
        self.findRegionMasks()

        ### get the center of the inner bull of the dart board
        label_img = label(self.myMask.inner_bull)
        region = regionprops(label_img)
        max_index = utils.get_max_index(region)
        center = region[max_index].centroid

        ### Edge image for straight line detection
        grayBackgroundImage = rgb2gray(self.boardImage)
        temp_image = grayBackgroundImage * self.myMask.board
        edgeImage = feature.canny(temp_image,high_threshold=0.4,low_threshold=0.2)
        tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 3600)
        [H,theta,rho] = transform.hough_line(edgeImage,theta=tested_angles)
        thresh = np.amax(H)
        thresh = np.ceil(thresh*0.05)
        
        ### Detect Peaks
        hspace, angle, dists = transform.hough_line_peaks(H,theta,rho,num_peaks=10,threshold=thresh)

        ##### change angles theta to degrees 
        theta_degree= np.degrees(angle)
        angles = []
        angles_180 =[]
        for a in theta_degree:
            angles.append(a-90+360)
            angles_180.append(a+90+360)
        
        ###  angles - Zero degrees = up 
        Angles = np.concatenate((angles,angles_180),axis=0)
        Angles = np.mod(Angles,360)
        Angles = np.sort(Angles)

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
        self.dartImage = utils.alignImages(self.dartImage,self.boardImage)
        
        ###### Difference of 2 Images 
        diff_image = utils.computeDifference(cv2.cvtColor(self.dartImage,cv2.COLOR_RGB2GRAY),cv2.cvtColor(self.boardImage,cv2.COLOR_RGB2GRAY))
        dart = np.multiply(diff_image,self.myMask.board)

        ####Find primary orientation of largest difference region
        [rows, columns, channels] = self.boardImage.shape
        dart_square = np.power(dart,2)
        SE = disk(np.round(rows/100))
        dart_square_threshed = dart_square > 0.2 * threshold_otsu(dart_square)
        self.myMask.dart = binary_dilation(dart_square_threshed,selem=SE)
        label_img = label(self.myMask.dart)
        region = regionprops(label_image=label_img)
        max_index = utils.get_max_index(region)

        #get the oriention in degrees
        orientation = region[max_index].orientation
        orientation = np.degrees(orientation)-90 # -90 to adjust the orientation

        #get the line structure elemet with orientation
        SE_line = utils.strel_line(length=50,degrees=orientation)

        #close using the line to get the true shape of dart touching the board
        self.myMask.dart = closing(dart_square_threshed,selem=SE_line)

        #get the contours of the dart then detect the extrem left point which is the point the dart touch the board in
        gray_dart = skimage.img_as_ubyte(self.myMask.dart)
        cnts = cv2.findContours(gray_dart, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        extLeft = tuple(c[c[:, :, 0].argmin()][0])

        ### compare the xhit and yhit of the dart with board to know which region the dart hit
        self.dartScore = self.find_hitRegion(xhit=extLeft[0],yhit=extLeft[1],center=center,region=regions_details)

        ### draw a contour of the hit region
        hit_region = skimage.img_as_ubyte(self.myMask.hit)
        cnts = cv2.findContours(hit_region, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cv2.drawContours(self.outputBoardImage, cnts, -1, (50, 255, 50), 8)




    def findRegionMasks(self):

        grayImage = rgb2gray(self.boardImage)
        image = skimage.img_as_float64(self.boardImage)

        ###detect red regions in the board
        redRegions = image[:,:,0]-grayImage
        self.myMask.red = redRegions > threshold_otsu(redRegions) -0.05

        ###detect green regions in the board
        greenRegions = image[:,:,1]-grayImage
        self.myMask.green = greenRegions > (-threshold_otsu(greenRegions)) - 0.05

        ###detect multipliers regions
        self.myMask.multipliers=self.myMask.red + self.myMask.green
        self.myMask.multipliers = skimage.img_as_float64(self.myMask.multipliers)
        SE = disk(np.round(np.size(image[:,1,1])/100))

        ###detect multrigns region
        self.myMask.multRings = binary_closing(self.myMask.multipliers,SE)
        self.myMask.multRings = skimage.img_as_float64(self.myMask.multRings)

        ### imfill holes of multrings  
        seed = np.copy(self.myMask.multRings)
        seed[1:-1, 1:-1] = self.myMask.multRings.max()
        mask = self.myMask.multRings
        self.myMask.board = reconstruction(seed, mask, method='erosion')
        change_to_bool = np.array(self.myMask.board , dtype=bool)
        self.myMask.miss= ~change_to_bool
        self.myMask.single = self.myMask.board-self.myMask.multRings

        #### imfill holes of self.myMask.single 
        seed = np.copy(self.myMask.single)
        seed[1:-1, 1:-1] = self.myMask.single.max()
        mask = self.myMask.single
        Tempp= reconstruction(seed, mask, method='erosion')
        self.myMask.double = self.myMask.board-Tempp

        ### inner Ring 
        inner_Ring  = self.myMask.board-self.myMask.double-self.myMask.single
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
        self.myMask.triple = self.myMask.board-self.myMask.double-self.myMask.single - Tempp
        self.myMask.triple[self.myMask.triple < 0] = 0

        ### outer Bull 
        self.myMask.outer_bull = (self.myMask.multRings - self.myMask.double - self.myMask.triple) * self.myMask.green
        
        #### inner Bull 
        self.myMask.inner_bull = (self.myMask.multRings - self.myMask.double - self.myMask.triple) * self.myMask.red

    


    def find_hitRegion(self,xhit, yhit, center, region):

        [rows, columns] =self.myMask.board.shape
        x = int(xhit)
        y = int(yhit)

        ### get the angle of the region the dart hit the board
        hitAngle = math.atan2(y-center[0],x-center[1])
        hitAngle = np.mod((hitAngle * 180 / math.pi) + 360 ,360)

        ###detect region contain the hit angle
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

        ### construct a mask for the region the dart hit
        x1,y1 = utils.pol2cart(phi=region[hitRegion].minAngle,rho=Max)
        x2,y2 = utils.pol2cart(phi=region[hitRegion].maxAngle,rho=Max)
        first_array = [center[1],x1+center[1],x2+center[1]]
        second_array = [center[0],y1+center[0],y2+center[0]]
        shape=[rows,columns]
        self.myMask.hit = utils.poly2mask(first_array,second_array,shape)

        score = region[hitRegion].value

        ###check if the dart hit a special region 
        if (self.myMask.single[y][x]):
            self.myMask.hit= np.multiply(self.myMask.single,self.myMask.hit)
        elif (self.myMask.double[y][x]):
            score = score * 2
            self.myMask.hit= np.multiply(self.myMask.double,self.myMask.hit)
        elif (self.myMask.triple[y][x]):
            score = score * 3
            self.myMask.hit= np.multiply(self.myMask.triple,self.myMask.hit)
        elif(self.myMask.miss[y][x]):
            score = 0 
            self.myMask.hit = self.myMask.miss
        elif(self.myMask.inner_bull[y][x]):
            score = 25
            self.myMask.hit = self.myMask.inner_bull
        elif(self.myMask.outer_bull[y][x]):
            score = 50
            self.myMask.hit = self.myMask.outer_bull
        
        self.myMask.hit = self.myMask.hit>0.5

        return score

    
    def get_score(self):
        return self.dartScore
    

    def get_outputImage(self):
        return self.outputBoardImage



if __name__ == "__main__":
    dartBoardImage = imread("../test_images/dartBoard2.jpg")
    dart_detection = Dart_Detection(dartBoardImage)
    dartImage = imread("../test_images/dart14.jpg")
    dart_detection.computeScore(dartImage)
    print(dart_detection.get_score())
    imshow(dart_detection.get_outputImage())
    plt.show()