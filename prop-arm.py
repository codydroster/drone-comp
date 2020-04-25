from inputs import get_gamepad
import serial
import serial.tools.list_ports
import threading
from time import sleep


class droneArm:

	pitch = 0
	
	


	def __init__(self):
		
		self.ser = serial.Serial('/dev/ttyS0')
		self.ser.baudrate = 115200


drone1 = droneArm()





while 1:
	

	data = drone1.ser.read()
	


	

	

	
		



