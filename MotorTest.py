import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time
import numpy as np

def ANG_read(a):
	b = np.zeros(10)
	for x in range(0, 10):
		b[x]=ADC.read(a)*360

	avg = round(sum(b)/10, 1)
	return avg 


read_pin = 'P9_40'

ADC.setup()
PWM.start("P8_13", 0)
PWM.start("P8_19", 0)

target = input('enter angle: ')
angle = ANG_read(read_pin)



while True:
	if angle < target-0.3 or angle > target+0.3:
		angle = ANG_read(read_pin)
		print('%f' % (angle))
		prop=target-angle
		if prop<0:
			if abs(prop) < 180:
				#Clockwise
				duty=round(abs(prop)/6)+70
				PWM.set_duty_cycle("P8_19", 0)
				PWM.set_duty_cycle("P8_13", duty)
			else:
				#Counter Clockwise
				duty=round((360-abs(prop))/6)+70
				PWM.set_duty_cycle("P8_13", 0)
				PWM.set_duty_cycle("P8_19", duty)
		else:
			if abs(prop) < 180:
				#Counter Clockwise
				duty=round(abs(prop)/6)+70
				PWM.set_duty_cycle("P8_13", 0)
				PWM.set_duty_cycle("P8_19", duty)
			else:
				#Clockwise
				duty=round((360-abs(prop))/6)+70
				PWM.set_duty_cycle("P8_19", 0)
				PWM.set_duty_cycle("P8_13", duty)
	else:
		PWM.set_duty_cycle("P8_19", 0)
		PWM.set_duty_cycle("P8_13", 0)
		angle = ANG_read(read_pin)
		print angle		

