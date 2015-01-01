from SimpleCV import *		#import all the SimpleCV libraries

cam = Camera(0, {"width" : 320, "height" : 240})	#create a camera object

display = Display()		#create a display object

while not display.isDone():		#loop infinitely until display window is closed

	img = cam.getImage()		#get an image from the camera
	
	flipped_img = img.flipHorizontal()		#flip the image Horizontally
	
	flipped_img.show()		#show it on the display window