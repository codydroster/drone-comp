import io
import os
import fileinput





f = open('/home/cody/Desktop/sol1.pos', 'r+')
f.readlines()
currentPos = f.tell()
f.close()

while 1:
	f = open('/home/cody/Desktop/sol1.pos', 'r+')
	f.seek(currentPos,0)
	line = f.readline()
	currentPos = f.tell()
	if(line is not ''):
		print(line[17:30])
		print(line[32:45])
		print(line[48:56])
	f.close()
