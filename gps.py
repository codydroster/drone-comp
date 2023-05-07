import io
import os
import time
import random

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



	def setFakeGPS(self):
		with open(self.filepath, 'w+') as f:
			f.seek(0,2)
			if(f.tell() == 0):
				line0 = '%  GPST                  latitude(deg) longitude(deg)  height(m)   Q  ns   sdn(m)   sde(m)   sdu(m)  sdne(m)  sdeu(m)  sdun(m) age(s)  ratio'
				f.write(line0)
				
			else:
				fixed_lat = 43.08
				random_part = random.uniform(0, 0.009999)  # Generates a random float between 0 and 0.000099 (inclusive)
				lat = fixed_lat + random_part

				fixed_long = -89.28
				random_part = random.uniform(0, 0.009999)  # Generates a random float between 0 and 0.000099 (inclusive)
				long = fixed_long + random_part

				fixed_alt = 290.
				random_part = random.uniform(0, 0.99)  # Generates a random float between 0 and 0.000099 (inclusive)
				alt = fixed_alt + random_part

				line1 = '2023/05/07 03:56:55.800   ' + str(lat) + '   ' +  str(long) + '   ' +  str(alt) + '   2   4   4.9783   3.2030   6.0352  -3.6976   1.3169  -3.0256   0.80    6.5'
				f.write(line1)
				f.write('\n')
				f.close()