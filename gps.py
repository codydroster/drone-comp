import io
import os
import fileinput


class GPS:

	def __init__(self, filepath):
		self.lat = 0
		self.long = 0
		self.alt = 0


		self.filepath = filepath
		f = open(filepath, 'r+')
		f.readlines()
		self.currentPos = f.tell()
		f.close()


	def getGPS(self):
		f = open('/home/cody/Desktop/sol1.pos', 'r+')
		f.seek(self.currentPos,0)
		line = f.readline()
		self.currentPos = f.tell()
		if(line is not ''):
			self.lat = (line[17:30])
			self.long = (line[32:45])
			self.alt = (line[48:56])
			f.close()			
	


#f = open('/home/cody/Desktop/sol1.pos', 'r+')
#f.readlines()
#currentPos = f.tell()
#f.close()

#while 1:
#	f = open('/home/cody/Desktop/sol1.pos', 'r+')
#	f.seek(currentPos,0)
#	line = f.readline()
#	currentPos = f.tell()
#	if(line is not ''):
#		print(line[17:30])
#		print(line[32:45])
#		print(line[48:56])
#	f.close()
