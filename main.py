from inputs import get_gamepad
import serial
import serial.tools.list_ports
import threading
from time import sleep


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
		self.ser.baudrate = 115200
		
		

	def update_attitude(self, rx_data):
		index_start = 0
		rx_aligned = []
		
		#determine where 10 byte packet begins.
		for i, byte in enumerate(rx_data):
			if byte is 0x42:
				index_start = i
				break
		
		
		
		if(index_start is 14):
			if(rx_data[0] is 0x43):
				rx_aligned = [rx_data[14], rx_data[0-13]]
				
				
		else:
			if(rx_data[index_start + 1] is 0x43):
				rx_aligned = [rx_data[index_start - 13], rx_data[0 - (index_start - 1)]]
				
					
		self.roll = int.from_bytes(rx_aligned[2-3])
		
		 
	

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
		bytes_tx.append((trans_real.throttle >> 8) & 0xff)
		bytes_tx.append(trans_real.throttle & 0xff)
		bytes_tx.append((trans_real.roll >> 8) & 0xff)
		bytes_tx.append(trans_real.roll & 0xff)
		bytes_tx.append((trans_real.pitch >> 8) & 0xff)
		bytes_tx.append(trans_real.pitch & 0xff)
		bytes_tx.append((trans_real.yaw >> 8) & 0xff)
		bytes_tx.append(trans_real.yaw & 0xff)
		bytes_tx.append((trans_real.sw_c >> 8) & 0xff)
		bytes_tx.append(trans_real.sw_c & 0xff)
		bytes_tx.append((trans_real.sw_d >> 8) & 0xff)
		bytes_tx.append(trans_real.sw_d & 0xff)
	
		bytarr = bytearray()
		
		for ele in bytes_tx:
			bytarr.append(ele)
		

		return bytarr
		
		
	def update_gamepad(self):
		while 1:	
			events = get_gamepad()
			for event in events:
				if event.code is "ABS_X":
					Transmitter.raw_yaw = event.state
					
				if event.code is "ABS_Y":
					Transmitter.raw_throttle = event.state

				if event.code is "ABS_RX":
					Transmitter.raw_pitch = event.state

				if event.code is "ABS_Z":
					Transmitter.raw_roll = event.state
					
				if event.code is "ABS_RY":
					Transmitter.raw_sw_c = event.state
			
				if event.code is "ABS_RZ":
					Transmitter.raw_sw_d = event.state
				

			Transmitter.throttle = int(2000/1362 * (trans_real.raw_throttle - 342))
			Transmitter.yaw = int(2000/1362 * (trans_real.raw_yaw - 342))
			Transmitter.pitch = int(2000/1362 * (trans_real.raw_pitch - 342))
			Transmitter.roll = int(2000/1362 * (trans_real.raw_roll - 342))
			if(Transmitter.raw_sw_c > 45):
				Transmitter.sw_c = 0
			else:
				Transmitter.sw_c = 1000
			
			if(Transmitter.raw_sw_d < 45):
				Transmitter.sw_d = 2000
			elif(210 > Transmitter.raw_sw_d > 45):
				Transmitter.sw_d = 1000
			elif(Transmitter.raw_sw_d > 210):
				Transmitter.sw_d = 0
			

	#		print(Transmitter.sw_d)
	

		


drone1 = Drone()
trans_real = Transmitter()
threading.Thread(target=trans_real.update_gamepad).start()



while 1:
	
	
	transmit_bytes = trans_real.transmit_bytes()


	drone1.ser.write(transmit_bytes)
	
	data = drone1.ser.read(10)
	
	drone1.update_attitude(data)
	
	print(drone1.roll)
	
#	sleep(.01)

	

	

	
		



