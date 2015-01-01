from SimpleCV import *		#import all the SimpleCV libraries

cam = Camera(0, {"width" : 320, "height" : 240})	#create a camera object

display = Display()		#create a display object

HUE = 0					#change this value between 0 and 255 to filter different colors

while not display.isDone():		#loop infinitely until display window is closed

	img = cam.getImage().flipHorizontal()		#capturing image and flipping horizontally
	
	hsv_img = img.toHSV()						#converting from RGB colorspace to HSV
	
	dist_img = hsv_img.hueDistance(HUE)			#finding distance from a particular HUE
	
	bin_img = dist_img.binarize(20)				#converting grayscale image to binary
	
	eroded_img = bin_img.erode()				#eroding image

	dilated_img = eroded_img.dilate()			#dilating image
	
	img.show()		#change this line to show dist_img, bin_img, eroded_img, dilated_img