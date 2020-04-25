import serial
import io
import os
import fileinput
import serial.tools.list_ports
	
	
os.remove('../rtk/rover.ubx')
f = open('../rtk/rover.ubx', 'wb')
	
	
port_list = serial.tools.list_ports.comports()
for i, port in enumerate(port_list):
	print(i, port.device)
selected_port = port_list[int(input("Choose Port: "))]
		
ser = serial.Serial(selected_port[0])
ser.baudrate = 230400	



while 1:
	
	while(ser.in_waiting is 0):
		None

	read0 = ser.read()

	if(read0 == b'B'):


		while(ser.in_waiting is 0):
			None
			
		read1 = ser.read()

		if(read1 == b'C'):
			rx_aligned = ser.read(8)
			roll = int.from_bytes(rx_aligned[0:2], byteorder='big', signed='true')
			pitch = int.from_bytes(rx_aligned[2:4], byteorder='big', signed='true')
			heading = int.from_bytes(rx_aligned[4:6], byteorder='big', signed='true') 
			altitude = int.from_bytes(rx_aligned[6:8], byteorder='big', signed='true')

			
			#great time to transmit, next ~600 byte packet 50ms away
			#ser.write(trans_real.transmit_bytes())

			
		else:
			f.write(read0)
			f.write(read1)
	else:
		f.write(read0)

