# DartsMobileApp
Android application based on Digital Image processing to detect darts scoring 

## Implementation
this project is implemented in python for the algorithm and flutter for the application GUI

## Background 
### Description of the Project Algorithm :
### First the user will input the first image without any dart on the board (background image)
<br>
<img src="test_images/dartBoard1.jpg" width="450">

### This image is proccessed to obtain the regions of the board respectively like : 
|multipliers |triple       |
|------------|-------------|
|<img src="debug_images/multipliers regions.jpg" width="450">|<img src="debug_images/triple regions.jpg" width="450">|

|double      |single       |
|------------|-------------|
|<img src="debug_images/double regions.jpg" width="450">|<img src="debug_images/sigle regions.jpg" width="450">|

|outerBull   |innerBull    |
|------------|-------------|
|<img src="debug_images/outerbull regions.jpg" width="450">|<img src="debug_images/innerbull regions.jpg" width="450">|

### Then the user inputs the board image that contains the dart want to detect it's score 
<br>
<img src="test_images/dart14.jpg" width="450">

### Align the two images (background - dart) using sift algorithm 

<img src="debug_images/matches.jpg" width="450">

### then get the difference between the two images to detect the the dart position and apply closing method 

|diff image  |after closing|
|------------|-------------|
|<img src="debug_images/diff image.jpg" width="450">|<img src="debug_images/affer closing with lin SE.jpg" width="450">|















## Installation
will be updated 








