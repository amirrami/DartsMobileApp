# DartsMobileApp
Android application based on Digital Image processing to detect darts scoring 

## Implementation
this project is implemented in python for the algorithm and flutter for the application GUI

## Background 
### description of the project algorithm :
### first the user will input the first image without any dart on the board (background image)
<br>
<img src="test_images/dartBoard1.jpg" width="250">
<br>
### this image is proccessed to obtain the regions of the board respectively like : 
<br>
|multipliers |double       |
|------------|-------------|
|<img src="debug_images/multipliers regions.jpg" width="250">|<img src="debug_images/double regions.jpg" width="250">|
<br>
### the user inputs the board image that contains the dart want to detect it's score 
<br>
<img src="test_images/dart11.jpg" width="250">
<br>
### align the two images (background - dart) using sift algorithm 
<img src="debug_images/matches.jpg" width="250">
<br>
### finally get the difference between the two images to detect the the dart position 
<br>
<img src="debug_images/diff image.jpg" width="250">
<br>












## Installation
will be updated 








