from inputs import devices 

class Transmitter:

	def __init__(self):

		self.raw_throttle = 345
		self.raw_yaw = 1024
		self.raw_pitch = 1024
		self.raw_roll = 1024
		self.raw_sw_c = 1024
		self.raw_sw_d = 1024
		

	#range: 0-2000
		self.throttle = 0
		self.yaw = 1000
		self.pitch = 1000
		self.roll = 1000
		self.sw_c = 0
		self.sw_d = 0

		self.hoverThrottle = 600
		self.autoHeading = 1500
		self.autoAltitude = 0



		
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

