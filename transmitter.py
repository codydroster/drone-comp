class Transmitter:


#range: 0-2000
	yaw = 0
	throttle = 1000
	roll = 1000
	pitch = 1000
	auxA = 0
	auxD = 0
	knobR = 0

	errorLAT = 0
	errorLONG = 0
	errorALT = 0


#	def __init__(self):
		
	def transmit_bytes(self):




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
		bytes_tx.append((self.knobR >> 8) & 0xff)
		bytes_tx.append(self.knobR & 0xff)

		bytes_tx.append((self.errorLAT >>8) & 0xff)
		bytes_tx.append(self.errorLAT & 0xff)
		bytes_tx.append((self.errorLONG >>8) & 0xff)
		bytes_tx.append(self.errorLONG & 0xff)
		bytes_tx.append((self.errorALT >>8) & 0xff)
		bytes_tx.append(self.errorALT & 0xff)
		
		bytes_tx.append(0x43)


		bytarr = bytearray()
		
		for ele in bytes_tx:
			bytarr.append(ele)
		
		return bytarr
