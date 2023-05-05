import io
import os
import time

class GPS:
	def __init__(self, filepath):
		self.lat = 0		
		self.long = 0
		self.alt = 0

		self.filepath = filepath
		self.file = open(self.filepath, 'r+')
		self.file.readlines()
		self.currentPos = self.file.tell()
    
	def getGPS(self):
		with open(self.filepath, 'r+') as f:
			f.seek(self.currentPos, 0)
			line = f.readline()
			self.currentPos = f.tell()
			if line != '':
				fields = line.split()
				self.lat = float(fields[2])
				self.long = float(fields[3])
				self.alt = float(fields[4])

				

gps = GPS('./position_data/rov.pos')

while True:
    gps.getGPS()
    print(gps.lat)
    time.sleep(.01)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
#     def getGPS(self):
#         attempts = 5
#         backoff_time = 0.05  # 50 milliseconds
#         success = False
#         while attempts > 0:
#             try:
#                 with open(self.filepath, 'r+') as f:
#                     f.seek(self.currentPos, 0)
#                     line = f.readline()
#                     self.currentPos = f.tell()
#                     if line != '':
#                         fields = line.split()
#                         self.lat = float(fields[2])
#                         self.long = float(fields[3])
#                         self.alt = float(fields[4])
#                         success = True
#                         break
#             except IOError:
#                 attempts -= 1
#                 time.sleep(backoff_time)
#                 backoff_time *= 2

#         if not success:
#             print("Failed to read GPS data after multiple attempts")

# gps = GPS('./position_data/rov.pos')

# while True:
#     gps.getGPS()
#     print(gps.lat)
#     time.sleep(.01)
