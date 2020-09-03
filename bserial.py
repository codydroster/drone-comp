from inputs import devices 
import serial
import serial.tools.list_ports
import threading
from time import sleep
import time
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
	
	throttle = 0
	roll = 0
	pitch = 0
	yaw = 0
	sw_c = 0
	sw_d = 0
	

	def __init__(self):
		self.ser1 = 0
		port_list = serial.tools.list_ports.comports()
		for i, port in enumerate(port_list):
			print(i, port.device)
		selected_port = port_list[int(input("Choose Port: "))]
		
		self.ser = serial.Serial(selected_port[0])
		self.ser.baudrate = 230400
		
		




def serial_handler():


	if(drone1.ser.in_waiting > 0):
	
		read0 = drone1.ser.read()
		
		if(read0 == b'B'):
			read1 = drone1.ser.read()
			
			if(read1 == b'C'):
				

	
				rx_aligned = drone1.ser.read(12)
				drone1.throttle = int.from_bytes(rx_aligned[0:2], byteorder='big', signed='true')
				drone1.roll = int.from_bytes(rx_aligned[2:4], byteorder='big', signed='true')
				drone1.pitch = int.from_bytes(rx_aligned[4:6], byteorder='big', signed='true') 
				drone1.yaw = int.from_bytes(rx_aligned[6:8], byteorder='big', signed='true')
				drone1.sw_c = int.from_bytes(rx_aligned[8:10], byteorder='big', signed='true')
				drone1.sw_d = int.from_bytes(rx_aligned[10:12], byteorder='big', signed='true')

				
				print(drone1.throttle)
			


drone1 = Drone()


while 1:

	serial_handler()


	
	

			
	
	
	
	
	
	
	
	
	
	
	
	
	
	



	

	

	
		



