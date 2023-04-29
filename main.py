from inputs import devices 
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

		if(self.sw_c == 0): #0
			bytes_tx = [0x42]
			bytes_tx.append((self.throttle >> 8) & 0xff)
			bytes_tx.append(self.throttle & 0xff)
			bytes_tx.append((self.roll >> 8) & 0xff)
			bytes_tx.append(self.roll & 0xff)
			bytes_tx.append((self.pitch >> 8) & 0xff)
			bytes_tx.append(self.pitch & 0xff)
			bytes_tx.append((self.yaw >> 8) & 0xff)
			bytes_tx.append(self.yaw & 0xff)

			bytes_tx.append((self.sw_c >> 8) & 0xff)
			bytes_tx.append(self.sw_c & 0xff)
			bytes_tx.append((self.sw_d >> 8) & 0xff)
			bytes_tx.append(self.sw_d & 0xff)
			bytes_tx.append(0x43)

			hoverThrottle = self.throttle
		
			bytarr = bytearray()
			
			for ele in bytes_tx:
				bytarr.append(ele)
			
			return bytarr
			
			
		if(self.sw_c > 0): #1000	AUXC switch on
			bytes_tx = [0x42]
			bytes_tx.append((self.throttle >> 8) & 0xff)
			bytes_tx.append(self.throttle & 0xff)
			bytes_tx.append((self.roll >> 8) & 0xff)
			bytes_tx.append(self.roll & 0xff)
			bytes_tx.append((self.pitch >> 8) & 0xff)
			bytes_tx.append(self.pitch & 0xff)
			bytes_tx.append((self.autoHeading >> 8) & 0xff)
			bytes_tx.append(self.autoHeading & 0xff)



	def update_gamepad(self):
		#Yaw (invert)
		value = int((-pyJoystick.get_axis(0) + .665) * 1503) 
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		self.yaw = value


		#Throttle
		value = int((pyJoystick.get_axis(1) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		self.throttle = value


		#Roll (invert)
		value = int((-pyJoystick.get_axis(0) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		self.roll = value


		#Pitch
		value = int((pyJoystick.get_axis(0) + .665) * 1503) 
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		self.pitch = value


		#AUX A
		value = int((-pyJoystick.get_axis(1) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		self.auxA = value


		#AUX D (invert)
		value = int((-pyJoystick.get_axis(0) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		self.auxD = value


		#Knob R
		value = int((-pyJoystick.get_axis(0) + .665) * 1503) #invert
		if(value > 2000):
			value = 2000
		elif(value < 0):
			value = 0
		self.knobR = value
		



def serial_handler():

	if(drone1.ser.in_waiting > 0):
	
		read0 = drone1.ser.read()

	
		if(read0 != b'B'):
			f.write(read0)
	
	
	#verify frame **need to simplify**
		else:
			rx_aligned = drone1.ser.read(9)
			
			if(rx_aligned[9] == 0x43): #maybe rx_aligned[9]
				if(drone1.roll > 1000 and drone1.roll < 2000):
					if(drone1.pitch > 1000 and drone1.pitch < 2000):
						if(drone1.heading < 3601):
							drone1.roll = int.from_bytes(rx_aligned[0:2], byteorder='big', signed='true')					
							drone1.pitch = int.from_bytes(rx_aligned[2:4], byteorder='big', signed='true')
							drone1.heading = int.from_bytes(rx_aligned[4:6], byteorder='big', signed='true') 
							drone1.altitude = int.from_bytes(rx_aligned[6:8], byteorder='big', signed='true')
							

							#great time to transmit, next ~600 byte packet 50ms away
							txbytes = trans_real.transmit_bytes()

							#send to drone
							if(txbytes is not None):
								drone1.ser.write(txbytes)
								print(trans_real.throttle)
						
						#only write to file if all if statments fail
						else:
							f.write(rx_aligned)
				


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

  

#	print(trans_real.throttle)




os.remove('/home/codyd/git/drone-comp/io/rover.ubx')
f = open('/home/codyd/git/drone-comp/io/rover.ubx', 'wb')
drone1 = Drone()
trans_real = Transmitter()
gps = GPS()

#get initial counter value
gps.pastTime = time.perf_counter()





while 1:

	serial_handler()
	pid_heading()
	trans_real.update_gamepad()
#	print(trans_real.throttle)
#	print(trans_real.sw_c)
#	print(trans_real.throttle)

	

			
	
	
	
	
	
	
	
	
	
	
	
	
	
	



	

	

	
		



