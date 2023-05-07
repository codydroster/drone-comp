import io
import os
import time

class GPS:
	def __init__(self, filepath):
		self.lat = 0		
		self.long = 0
		self.alt = 0
		try:
			self.filepath = filepath
			self.file = open(self.filepath, 'r+')
			self.file.readlines()
			self.currentPos = self.file.tell()
		except:
			print(self.filepath, 'not available')

	def getGPS(self):
		try:
			with open(self.filepath, 'r+') as f:
				f.seek(self.currentPos, 0)

				line = f.readline()
				self.currentPos = f.tell()
				if line != '':
					fields = line.split()
					self.lat = float(fields[2])
					self.long = float(fields[3])
					self.alt = float(fields[4])
				f.close()
		except:
			print(self.filepath, 'not available')
				

# gps = GPS('./position_data/rover.pos')

