# DartsMobileApp
Android application based on Digital Image processing to detect darts scoring 
##Team Members : 
Amir rami zaref
Andrew atef fathy
Andrew morcos nagib

## Implementation
this project is implemented in python for the algorithm and flutter for the application GUI

## Background 
### Description of the Project Algorithm :
### First: the user will input the first image without any dart on the board like this image (background image)
<br>
<img src="test_images/dartBoard1.jpg" width="400">
### This image is proccessed to get the regions of interest:
first we get the red and green regions of the image then by adding these regions we get the multipliers then by making some 
morpholigical and diffrenences changes on these images we obtain the following regions acts as a mask for our work 
|Red         |Green        |
|------------|-------------|
|<img src="debug_images/red regions.jpg" width="400">|<img src="debug_images/green regions.jpg" width="400">|
<br>
|multipliers |triple       |
|------------|-------------|
|<img src="debug_images/multipliers regions.jpg" width="400">|<img src="debug_images/triple regions.jpg" width="400">|
<br>
|double      |single       |
|------------|-------------|
|<img src="debug_images/double regions.jpg" width="400">|<img src="debug_images/sigle regions.jpg" width="400">|
<br>
|outerBull   |innerBull    |
|------------|-------------|
|<img src="debug_images/outerbull regions.jpg" width="400">|<img src="debug_images/innerbull regions.jpg" width="400">|
<br>

### Then the user inputs the board image that contains the dart want to detect it's score 
<br>
<img src="test_images/dart14.jpg" width="400">

### Align the two images 
aligning the background and the dart image to make the dart image very close to the background image
<br>
<img src="debug_images/matches.jpg" width="400">

### Detect 20 Sectors of the board 
Detect the 20 Straight lines and their angles of interest 
<br>
<img src="debug_images/detectd lines.jpg" width="400">

### then get the difference between the two images to detect the the dart position and apply closing method 
<br>
|diff image  |after closing|
|------------|-------------|
|<img src="debug_images/diff image.jpg" width="400">|<img src="debug_images/affer closing with lin SE.jpg" width="400">|

### Then using the region props we detect the Apex of the arrow and it's coordinates and orientation 

### Finally This is the output : 
<br>
<img src="debug_images/Final Output.JPG" width="400">















## Installation
will be updated 








