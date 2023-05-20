
import pygame
import serial
import serial.tools.list_ports
import sys
import os
import argparse

from transmitter import Transmitter
from drone import Drone, Target
from gps import GPS

import time
import io
import os
import fileinput




def update_gamepad():
	#Yaw (invert)
	value = int((-pyJoystick.get_axis(0) + .665) * 1503) 
	if(value > 2000):
		value = 2000
	elif(value < 0):
		value = 0
	trans_real.yaw = value


	#Throttle
	value = int((pyJoystick.get_axis(1) + .665) * 1503) #invert
	if(value > 2000):
		value = 2000
	elif(value < 0):
		value = 0
	trans_real.throttle = value


	#Roll (invert)
	value = int((-pyJoystick.get_axis(2) + .665) * 1503) #invert
	if(value > 2000):
		value = 2000
	elif(value < 0):
		value = 0
	trans_real.roll = value


	#Pitch
	value = int((pyJoystick.get_axis(3) + .665) * 1503) 
	if(value > 2000):
		value = 2000
	elif(value < 0):
		value = 0
	trans_real.pitch = value


	#AUX A
	value = int((-pyJoystick.get_axis(4) + .665) * 1503) #invert
	if(value > 2000):
		value = 2000
	elif(value < 0):
		value = 0
	trans_real.auxA = value


	#AUX D (invert)
	value = int((-pyJoystick.get_axis(5) + .565) * 1503) #invert
	if(value > 2000):
		value = 2000
	elif(value < 0):
		value = 0
	trans_real.auxD = value


	#Knob R
	value = int((pyJoystick.get_axis(7) + .665) * 1503) #invert
	if(value > 2000):
		value = 2000
	elif(value < 0):
		value = 0
	trans_real.knobR = value



def serial_handler_rec():
	global tx_timer1
	rx_m4 = bytearray(11)
	if(drone1.ser.in_waiting > 0):

		read0 = drone1.ser.read()

	
		if(read0 == b'B'):
			rx_m4 = drone1.ser.read(11)

		
			if(rx_m4[0] == 67 and rx_m4[1] == 68 and rx_m4[10] == 69):
			
				drone1.roll = int.from_bytes(rx_m4[3:5], byteorder='big', signed='true')					
				drone1.pitch = int.from_bytes(rx_m4[4:6], byteorder='big', signed='true')
				drone1.heading = int.from_bytes(rx_m4[6:8], byteorder='big', signed='true') 
				drone1.altitude = int.from_bytes(rx_m4[8:10], byteorder='big', signed='true')
				
				# print(drone1.roll)
				
			else:
				f.write(rx_m4)		
		else:
			f.write(read0)
						#send to drone
	
	current_time = time.process_time()
	if(((current_time - tx_timer1) > .01)):
		txbytes = trans_real.transmit_bytes()
		if(txbytes is not None):
			drone1.ser.write(txbytes)
		tx_timer1 = time.process_time()
	time.sleep(.001)
		

def serial_handler():
	global tx_timer1
	
	if(drone1.ser.in_waiting > 10):
		f = open('./io/rover.ubx', 'ab')
		read = drone1.ser.read(drone1.ser.in_waiting)

		f.write(read)
		f.close()

	if args.o != 'notarget':	
		if(target1.ser.in_waiting > 10):
			f1 = open('./io/target.ubx', 'ab')
			read = target1.ser.read(target1.ser.in_waiting)

			f1.write(read)
			f1.close
						
	current_time = time.process_time()
	if(((current_time - tx_timer1) > .01)):
		txbytes = trans_real.transmit_bytes()
		if(txbytes is not None):
			drone1.ser.write(txbytes)
		tx_timer1 = time.process_time()
	time.sleep(.001)


def transmit_fake_data():
	#great time to transmit, next ~600 byte packet 50ms away
	txbytes = trans_real.transmit_bytes()

	#send to drone
	if(txbytes is not None):
		drone1.ser.write(txbytes)
		print(trans_real.throttle)



def calculate_error():

	scaleFactor = 10000000 		# 1cm per unit
	scaleFactorAlt = 100
	droneGPS.getGPS()
	targetGPS.getGPS()

	latError = int(droneGPS.lat*scaleFactor - targetGPS.lat*scaleFactor)
	longError = int(droneGPS.long*scaleFactor - targetGPS.long*scaleFactor)
	altError = int(droneGPS.alt*scaleFactorAlt - targetGPS.alt*scaleFactorAlt)

#	return [latError, longError, altError]
	return [309, 309, 0]





parser = argparse.ArgumentParser()
parser.add_argument('-o', choices=['noctl', 'notarget'])

args = parser.parse_args()

if args.o != 'noctl':
		pygame.init()
		pygame.joystick.init()
		pyJoystick = pygame.joystick.Joystick(0)


#test if valid
if os.path.exists('./io/rover.ubx'):
	os.remove('./io/rover.ubx')



if os.path.exists('./io/target.ubx'):
	os.remove('./io/target.ubx')
	f1 = open('./io/target.ubx', 'wb')

else:
	f1 = open('./io/target.ubx', 'wb')
	
drone1 = Drone()
if args.o != 'notarget':
	target1 = Target()
trans_real = Transmitter()
droneGPS = GPS('./position_data/rover.pos')
targetGPS = GPS('./position_data/target.pos')
#targetGPS.lat = 43.089602
#targetGPS.long = -89.282316
#targetGPS.alt = 350


tx_timer1 = time.process_time()
tx_timer2 = time.process_time()


while(True):


	serial_handler()
	if args.o != 'noctl':
		pygame.event.pump()
		update_gamepad() 
		
	
	current_time = time.process_time()
	if(((current_time - tx_timer2) > .01)):
		error = calculate_error()
		trans_real.errorLAT = min(500, (max(error[0], -500)))	#pitch
		trans_real.errorLONG = min(500, (max(error[1], -500)))	#roll
		trans_real.errorALT = min(500, (max(error[2], -500)))

		print(str(trans_real.errorLAT) + '  ' + str(trans_real.errorLONG))	
#		print(droneGPS.lat)
		
		tx_timer2 = time.process_time()
	time.sleep(.002)

	
