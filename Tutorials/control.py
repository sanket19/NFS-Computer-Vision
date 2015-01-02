"""	Control Program for NFS with Computer Vision project
	This program detects the game controller, calculates its size and angle and writes
	the generated data to a temp file
	
	Author - Sanket Rajan Gupte
	Email  - sanketgupte14@gmail.com """

from SimpleCV import *	#importing SimpleCV libraries

cam = Camera(1, {"width":320, "height":240})	#Camera initialization. Using 1 for the external USB camera. Replace with 0 for inbuilt webcam
HUE = 165 										#Hue value of controller's color. Obtain this value from the calibrate.py program
FILE = "C:/Temp/control.txt"					#Temp file for writing control signals. Make sure Python is able to write to this location

""" This function captures an image from the camera, preprocesses it for the next stage - blob detection, and then returns the processed image """
def captureImage():

	#Adjust the binarization threshold and number of erodes and dilates to improve color detection
	return cam.getImage().flipHorizontal().toHSV().hueDistance(HUE).binarize(17).erode().dilate(3)
	
""" This function accepts an image, looks for blobs and returns size and angle of the largest blob """	
def getData(img):
	
	blobs = img.findBlobs(minsize = 2000)	#Looking for blobs. Change minsize threshold to suit your needs
	
	if blobs is not None:					#Ensure that blobs have been found
		angle = blobs[-1].angle()			#Calculate the angle made by the largest blob
		size = blobs[-1].area()				#Calculate area of the largest blob
	
	else:
		angle = 0							#set default values if no blob is found
		size = 0
		
	return size, angle

""" This function computes the %power for the turn based on angle along with a flag representing forward motion """
def writeData(size, angle):

	if size >= 5000:	#Check the size of the blob and set the flag for forward motion. Vary the threshold value to change performance
		fwd = "1"
	else:
		fwd = "0"
		
	if angle > 0:		#Check if the controller was tilted to the left or the right and set the appropriate flags
		L = "1"
		R = "0"
		
	elif angle < 0:
		L = "0"
		R = "1"
		
	else:
		L = "0"
		R = "0"
		
	angle = abs(angle)	#compute absolute value of angle
	pwm = min(100, int(100 * angle / 30))	#function mapping angle values from 0 - 30 to a percentage from 0 - 100.
	
	control = fwd + L + R	#generating the control signal string
	
	try:
		with open(FILE, "w") as file:		#open temp file for writing
			file.write(control + "\n")		#write data to the file
			file.write(str(pwm))
	except:									#Ignoring errors since there will be clashes with the C# program reading the file
		pass

""" This is the main function tying all the individual parts together """
def main():
		
	print "Starting program"
	
	try:
		while True:

			img = captureImage()
			size, angle = getData(img)
			writeData(size, angle)
						
	except KeyboardInterrupt:		#for clean shutdown when Ctrl + C is pressed to stop the program
		print "Program terminated"

main()	#Running the main function