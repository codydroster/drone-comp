def pid_heading():

	if(drone1.heading > 1800):
		drone1.heading = drone1.heading- 3600

	kP = .2
	setPoint = 0
	
	trans_real.autoHeading = int(1000 - drone1.heading * kP)
	
#	print(trans_real.autoHeading)



def pid_altitude():
	kP = 1 
	kI = .1 
	setPoint = 245
	minThrottle = 500
	maxThrottle = 1200
	maxOutput = 1500
	
	error = setPoint - gps.altitude
	drone1.pastTime = time.perf_counter() - drone1.pastTime

# P-Term
	proportional = error*Kp


#integrator anti-windup I-Term
#if condititions are met, use past value of integral

	if(error > 0 and integral > 0):
		if(drone1.output < maxOutput):	
			drone1.pastInt = error*drone1.pastTime*kI
	
	if(error < 0 and integral < 0):
		if(drone1.output < maxOutput):
			drone1.pastInt = error*drone1.pastTime*kI

	
		

	drone1.output = int(drone1.hoverThrottle + proportional + drone1.pastInt)
	drone1.autoAltitude = min(max(minThrottle, drone1.output), maxThrottle)
