import serial
import serial.tools.list_ports



#available_ports = serial.tools.list_ports.comports()


#for port in available_ports:
#	print(port.device)



ser1 = serial.Serial('/dev/ttyUSB0')

ser1.baudrate = 115200
ser1.bytesize = serial.EIGHTBITS
ser1.parity = serial.PARITY_NONE
ser1.stopbits = serial.STOPBITS_ONE
ser1.close()
ser1.open()

roll = 0

while(True):

#	print(byteread)
	if(ser1.read() == b'B'):
#		print(ser1.read())
		if(ser1.read() == b'C'):
		#read next 8 bytes
			pitchLSB = ser1.read()
			pitchMSB = ser1.read()
			rollLSB = ser1.read()
			rollMSB = ser1.read()
			yawLSB = ser1.read()
			yawMSB = ser1.read()

		#	roll |= rollMSB << 0x8
		#	roll |= rollLSB & 0xff

			pitch = int.from_bytes(pitchLSB + pitchMSB, "big", signed=True)
			roll = int.from_bytes(rollLSB + rollMSB, "big", signed=True)
			yaw = int.from_bytes(yawLSB + yawMSB, "big", signed=True)

		
			print(yaw)
			
#		print(ser1.read())
#	print(ser1.in_waiting)

#			port = self.serialportbox.useport
#			port.__init__()
#			port.port = self.serialportbox.edit.get_text()
#			port.baudrate = int(serialinfo[0])
#			port.bytesize = int(serialinfo[1])
#			port.parity = serialinfo[2][0]
#			port.stopbits = int(serialinfo[3])
