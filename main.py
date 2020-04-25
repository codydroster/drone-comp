from inputs import get_gamepad
import serial
import serial.tools.list_ports
import threading
from time import sleep
import io
import os
import fileinput
import multiprocessing as mp



class Drone:

	pitch = 0
	roll = 0
	yaw = 0
	heading = 0
	altitude = 0
	


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
	
	throttle = 1000
	yaw = 1000
	pitch = 1000
	roll = 1000
	sw_c = 1000
	sw_d = 1000



#	def __init__(self):
		
	def transmit_bytes(self):

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
	
		bytarr = bytearray()
		
		for ele in bytes_tx:
			bytarr.append(ele)
		

		return bytarr
		
		
	def update_gamepad(self):
		while 1:
	
			events = get_gamepad()
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

	while 1:

		while(drone1.ser.in_waiting is 0):
			None

		read0 = drone1.ser.read()
	#	print(read0)
		
		if(read0 == b'B'):

			while(drone1.ser.in_waiting is 0):
				None
				
			read1 = drone1.ser.read()

			if(read1 == b'C'):
				rx_aligned = drone1.ser.read(8)
				drone1.roll = int.from_bytes(rx_aligned[0:2], byteorder='big', signed='true')
				drone1.pitch = int.from_bytes(rx_aligned[2:4], byteorder='big', signed='true')
				drone1.heading = int.from_bytes(rx_aligned[4:6], byteorder='big', signed='true') 
				drone1.altitude = int.from_bytes(rx_aligned[6:8], byteorder='big', signed='true')

				#print(trans_real.transmit_bytes())
				#great time to transmit, next ~600 byte packet 50ms away
				txbytes = trans_real.transmit_bytes()
				#print(txbytes)
				drone1.ser.write(txbytes)
				while(drone1.ser.out_waiting is not 0):
					None
				
			else:
				f.write(read0)
				f.write(read1)
		else:
			
			f.write(read0)


os.remove('/home/cody/git/rtk/rover.ubx')
f = open('/home/cody/git/rtk/rover.ubx', 'wb')
drone1 = Drone()
trans_real = Transmitter()

threading.Thread(target=trans_real.update_gamepad).start()



while 1:
	serial_handler()
	
	

			
	
	
	
	
	
	
	
	
	
	
	
	
	
	



	

	

	
		



