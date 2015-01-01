"""	Calibration Program for NFS with Computer Vision project
	This program allows you to calibrate your controller by finding its hue value.
	It also shows you the frame rate
	Press the left and right mouse buttons to change the hue value.
	
	Author - Sanket Rajan Gupte
	Email  - sanketgupte14@gmail.com """
	
from SimpleCV import *	#importing SimpleCV libraries
from time import time	#importing time function to calculate frame rate

cam = Camera(1, {"width":320, "height":240})	#Camera initialization. Using 1 for the external USB camera. Replace with 0 for inbuilt webcam

display = Display()		#display object creation

print "Ready for Calibration ... Press ESC to exit"

HUE = 165	#Set this value to the approximate hue value of your controller

fps = 0
ot = 0

while not display.isDone():
	
	img = cam.getImage().flipHorizontal().toHSV().hueDistance(HUE).binarize(17).erode().dilate(3)	#Color filtering based on the hue value
	
	img.drawText(text = "Press Left and Right mouse buttons", x = 0, y = 0, color=(255, 0, 0), fontsize = 24)
	img.drawText(text = "HUE = " + str(HUE), x = 0, y = 30, color=(255, 0, 0), fontsize = 24)
	img.drawText(text = "FPS = " + str(fps), x = 0, y = 60, color=(255, 0, 0), fontsize = 24)
	
	img.show()
		
	if display.mouseLeft:
		HUE = HUE + 1
	
	elif display.mouseRight:
		HUE = HUE -1

	nt = time()				#calculating the frame rate
	fps = 1.0 / (nt - ot)
	ot = nt
	