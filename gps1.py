import io
import os
import time
from gps import GPS


gps = GPS('./position_data/rover.pos')
gpsTarget = GPS('./position_data/target.pos')

f = open('./position_data/rover.pos', 'r+')


while True:
	gps.setFakeGPS(f)
#	gpsTarget.setFakeGPS()
#	print(gps.lat)
	time.sleep(.2)
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
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
