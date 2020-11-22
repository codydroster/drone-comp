from inputs import devices 
import serial
import serial.tools.list_ports
import threading

import time
import io
import os
import fileinput
import multiprocessing as mp



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
		selected_port = port_list[int(input("Choose Port: "))]
		
		self.ser = serial.Serial(selected_port[0])
		self.ser.baudrate = 230400
		
		



class Transmitter:

	raw_throttle = 345
	raw_yaw = 1024
	raw_pitch = 1024
	raw_roll = 1024
	raw_sw_c = 1024
	raw_sw_d = 1024
	

#range: 0-2000
	throttle = 0
	yaw = 1000
	pitch = 1000
	roll = 1000
	sw_c = 0
	sw_d = 0

	hoverThrottle = 600
	autoHeading = 1500
	autoAltitude = 0


#	def __init__(self):
		
	def transmit_bytes(self):


		if(self.sw_c is 0): #0
			bytes_tx = [0x42, 0x43]
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

			hoverThrottle = self.throttle
		
			bytarr = bytearray()
			
			for ele in bytes_tx:
				bytarr.append(ele)
			
			return bytarr
			
			
		if(self.sw_c > 0): #1000	AUXC switch on
			bytes_tx = [0x42, 0x43]
			bytes_tx.append((self.throttle >> 8) & 0xff)
			bytes_tx.append(self.throttle & 0xff)
			bytes_tx.append((self.roll >> 8) & 0xff)
			bytes_tx.append(self.roll & 0xff)
			bytes_tx.append((self.pitch >> 8) & 0xff)
			bytes_tx.append(self.pitch & 0xff)
			bytes_tx.append((self.autoHeading >> 8) & 0xff)
			bytes_tx.append(self.autoHeading & 0xff)
			bytes_tx.append((self.sw_c >> 8) & 0xff)
			bytes_tx.append(self.sw_c & 0xff)
			bytes_tx.append((self.sw_d >> 8) & 0xff)
			bytes_tx.append(self.sw_d & 0xff)
		
			bytarr = bytearray()
			
			for ele in bytes_tx:
				bytarr.append(ele)
			
			return bytarr
			
			
			
		
		
	def update_gamepad(self):
		while 1:
	

			events = devices.gamepads[0]._do_iter()
			if events is not None:
				for event in events:
					if event.code is "ABS_X":
						self.raw_yaw = event.state	
					if event.code is "ABS_Y":
						self.raw_throttle = event.state
					if event.code is "ABS_RX":
						self.raw_pitch = event.state
					if event.code is "ABS_Z":
						self.raw_roll = event.state						
					if event.code is "ABS_RY":
						self.raw_sw_c = event.state			
					if event.code is "ABS_RZ":
						self.raw_sw_d = event.state
					

				self.throttle = int(2000/1362 * (self.raw_throttle - 342))
				self.yaw = int(2000/1362 * (self.raw_yaw - 342))
				self.pitch = int(2000/1362 * (self.raw_pitch - 342))
				self.roll = int(2000/1362 * (self.raw_roll - 342))
				
				if(self.raw_sw_c > 45):
					self.sw_c = 0
				else:
					self.sw_c = 1000
				
				if(self.raw_sw_d < 45):
					self.sw_d = 2000
				elif(210 > self.raw_sw_d > 45):
					self.sw_d = 1000
				elif(self.raw_sw_d > 210):
					self.sw_d = 0




def serial_handler():


	if(drone1.ser.in_waiting > 0):
	
		read0 = drone1.ser.read()

	
		if(read0 != b'B'):
			f.write(read0)
	
		else:
			read1 = drone1.ser.read()
			read2 = drone1.ser.read()
			read3 = drone1.ser.read()
	

			if(read1 == b'C'):
				if(read2 == b'D'):
					if(read3 == b'E'):
				
						rx_aligned = drone1.ser.read(8)
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

					else:
						f.write(read0)
						f.write(read1)
						f.write(read2)
						f.write(read3)
			
		
			

			
		
	 


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




os.remove('/home/cody/dev/RTK/rover.ubx')
f = open('/home/cody/dev/RTK/rover.ubx', 'wb')
drone1 = Drone()
trans_real = Transmitter()
gps = GPS()

#get initial counter value
gps.pastTime = time.perf_counter()

#inputs module blocks
threading.Thread(target=trans_real.update_gamepad).start()



while 1:

	serial_handler()
	pid_heading()
#	print(trans_real.throttle)
#	print(trans_real.sw_c)
#	print(trans_real.throttle)

	

			
	
	
	
	
	
	
	
	
	
	
	
	
	
	



	

	

	
		



