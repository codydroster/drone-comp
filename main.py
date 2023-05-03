
import pygame
import serial
import serial.tools.list_ports


import time
import io
import os
import fileinput
import multiprocessing as mp


pygame.init()
pygame.joystick.init()
pyJoystick = pygame.joystick.Joystick(0)


class GPS:
	longitude = 0
	latitude = 0
	altitude = 0
	pastTime = 0

class Drone:

	pitch = 0
	roll = 0
	yaw = 0
	heading = 0
	altitude = 0
	altitudeInt = 0	
	output = 0


	def __init__(self):
		self.ser1 = 0
		port_list = serial.tools.list_ports.comports()
		for i, port in enumerate(port_list):
			print(i, port.device)
		selected_port = port_list[int(input("Choose Xbee Port: "))]
		
		self.ser = serial.Serial(selected_port[0])
		self.ser.baudrate = 230400
		self.ser.timeout = 60
		
		
def update_gamepad():
		#Yaw (invert)
		value = int((-pyJoystick.get_axis(0) + .665) * 1503) 
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		trans_real.yaw = value


		#Throttle
		value = int((pyJoystick.get_axis(1) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		trans_real.throttle = value


		#Roll (invert)
		value = int((-pyJoystick.get_axis(2) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		trans_real.roll = value


		#Pitch
		value = int((pyJoystick.get_axis(3) + .665) * 1503) 
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		trans_real.pitch = value


		#AUX A
		value = int((-pyJoystick.get_axis(4) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		trans_real.auxA = value


		#AUX D (invert)
		value = int((-pyJoystick.get_axis(5) + .565) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		trans_real.auxD = value


		#Knob R
		value = int((-pyJoystick.get_axis(6) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		trans_real.knobR = value


class Transmitter:


#range: 0-2000
	yaw = 0
	throttle = 1000
	roll = 1000
	pitch = 1000
	auxA = 0
	auxD = 0
	knobR = 0

	hoverThrottle = 600
	autoHeading = 1500
	autoAltitude = 0


#	def __init__(self):
		
	def transmit_bytes(self):

######also need to send waypoint info###############


		bytes_tx = [0x42]
		bytes_tx.append(0x42);
		bytes_tx.append(0x43);
		bytes_tx.append((self.throttle >> 8) & 0xff)
		bytes_tx.append(self.throttle & 0xff)
		bytes_tx.append((self.roll >> 8) & 0xff)
		bytes_tx.append(self.roll & 0xff)
		bytes_tx.append((self.pitch >> 8) & 0xff)
		bytes_tx.append(self.pitch & 0xff)
		bytes_tx.append((self.yaw >> 8) & 0xff)
		bytes_tx.append(self.yaw & 0xff)

		bytes_tx.append((self.auxA >> 8) & 0xff)
		bytes_tx.append(self.auxA & 0xff)
		bytes_tx.append((self.auxD >> 8) & 0xff)
		bytes_tx.append(self.auxD & 0xff)
		bytes_tx.append(0x43)

		hoverThrottle = self.throttle
	
		bytarr = bytearray()
		
		for ele in bytes_tx:
			bytarr.append(ele)
		
		return bytarr


def serial_handler():

	rx_m4 = bytearray(11)
	if(drone1.ser.in_waiting > 0):
		print('rec')
		read0 = drone1.ser.read()

	
		if(read0 == b'B'):
			drone1.ser.readinto(rx_m4)
		else:
			f.write(read0)

		if(rx_m4[0] == b'C' and rx_m4[1] == b'D' and rx_m4[10] == b'E'):
			drone1.roll = int.from_bytes(rx_m4[2:4], byteorder='big', signed='true')					
			drone1.pitch = int.from_bytes(rx_m4[4:6], byteorder='big', signed='true')
			drone1.heading = int.from_bytes(rx_m4[6:8], byteorder='big', signed='true') 
			drone1.altitude = int.from_bytes(rx_m4[8:10], byteorder='big', signed='true')
			

			#great time to transmit, next ~600 byte packet 50ms away
			txbytes = trans_real.transmit_bytes()

						#send to drone
			if(txbytes is not None):
				drone1.ser.write(txbytes)
				
		#only write to file if all if statments fail
		else:
			f.write(rx_m4)
				

def transmit_fake_data():
	#great time to transmit, next ~600 byte packet 50ms away
	txbytes = trans_real.transmit_bytes()

	#send to drone
	if(txbytes is not None):
		drone1.ser.write(txbytes)
		print(trans_real.throttle)


def pid_heading():

	if(drone1.heading > 1800):
		drone1.heading = drone1.heading- 3600

	kP = .2
	setPoint = 0
	
	trans_real.autoHeading = int(1000 - drone1.heading * kP)
	
#	print(trans_real.autoHeading)



def pid_altitude():
	kP = 1 
	kI = .1 
	setPoint = 245
	minThrottle = 500
	maxThrottle = 1200
	maxOutput = 1500
	
	error = setPoint - gps.altitude
	drone1.pastTime = time.perf_counter() - drone1.pastTime

# P-Term
	proportional = error*Kp


#integrator anti-windup I-Term
#if condititions are met, use past value of integral

	if(error > 0 and integral > 0):
		if(drone1.output < maxOutput):	
			drone1.pastInt = error*drone1.pastTime*kI
	
	if(error < 0 and integral < 0):
		if(drone1.output < maxOutput):
			drone1.pastInt = error*drone1.pastTime*kI

	
		

	drone1.output = int(drone1.hoverThrottle + proportional + drone1.pastInt)
	drone1.autoAltitude = min(max(minThrottle, drone1.output), maxThrottle)

  



os.remove('/home/cody/git/drone-comp/io/rover.ubx')
f = open('/home/cody/git/drone-comp/io/rover.ubx', 'wb')
drone1 = Drone()
trans_real = Transmitter()
gps = GPS()

#get initial counter value
gps.pastTime = time.perf_counter()





while(True):

	serial_handler()
#	print(drone1.ser.in_waiting)
	pid_heading()
	pygame.event.pump()
	update_gamepad()
#	print(trans_real.throttle)
#	print(trans_real.sw_c)
#	print(trans_real.throttle)

	

			
	
	
	
	
	
	
	
	
	
	
	
	
	
	



	

	

	
		



