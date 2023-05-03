import serial
import serial.tools.list_ports
import os

class Drone:


	def __init__(self, filepath):
		os.remove(filepath)
		self.f = open('/home/cody/dev/RTK/rover.ubx', 'wb')
		self.pitch = 0
		self.roll = 0
		self.yaw = 0
		self.heading = 0
		self.altitude = 0
		self.altitudeInt = 0	
		self.output = 0



		port_list = serial.tools.list_ports.comports()
		for i, port in enumerate(port_list):
			print(i, port.device)
		selected_port = port_list[int(input("Choose Port: "))]
		
		self.ser = serial.Serial(selected_port[0])
		self.ser.baudrate = 230400
		
		


	def serial_handler():


		if(self.ser.in_waiting > 0):
			
			read0 = self.ser.read()

		
			if(read0 != b'B'):
				self.f.write(read0)
		
			else:
				read1 = self.ser.read()
				read2 = self.ser.read()
				read3 = self.ser.read()
		

				if(read1 == b'C'):
					if(read2 == b'D'):
						if(read3 == b'E'):
					
							rx_aligned = drone1.ser.read(8)
							self.roll = int.from_bytes(rx_aligned[0:2], byteorder='big', signed='true')
							self.pitch = int.from_bytes(rx_aligned[2:4], byteorder='big', signed='true')
							self.heading = int.from_bytes(rx_aligned[4:6], byteorder='big', signed='true') 
							self.altitude = int.from_bytes(rx_aligned[6:8], byteorder='big', signed='true')
							
							return 1

							

						else:
							self.f.write(read0)
							self.f.write(read1)
							self.f.write(read2)
							self.f.write(read3)
