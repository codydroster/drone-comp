import gps


gpsDrone = gps.GPS('/home/cody/Desktop/sol1.pos')

while(1):
	gpsDrone.getGPS()

