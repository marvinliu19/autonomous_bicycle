import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.UART as UART
import numpy as np
import time 
import serial
import struct 

##############################################################################

def bit_check(a):
	c = ""
	for x in range(0,len(a)):
		b = hex(ord(a[x])).lstrip("0x") or "0"
		if len(b) != 2:
			b = '0'+b

		c = c+b

	return c

def imu_convert(a):
	d = struct.unpack('!f', a.decode('hex'))[0]
	return d 

def check_sum(a):
	b = 0
	for x in range(0,29):
		b= ord(a[x])+b
		
	c = hex(ord(a[29])).lstrip("0x") or "0"
	d = hex(ord(a[30])).lstrip("0x") or "0"
	e = int(c+d, 16)
	if e == b:
		f = 1
	else:	
		f = 0

	return f

def ANG_read(a):
	b = np.zeros(10)
	for x in range(0, 10):
		b[x] = ADC.read(a)*360

	avg = round(sum(b)/10, 1)
	return avg

def motor_set(a, b):
	prop = a-b
	if prop < 0:
		if abs(prop) < 180:
			duty = round(abs(prop)/6)+70
			PWM.set_duty_cycle("P8_19", 0)
			PWM.set_duty_cycle("P8_13", duty)
		else:
			duty = round((360-abs(prop))/6)+70
			PWM.set_duty_cycle("P8_13", 0)
			PWM.set_duty_cycle("P8_19", duty)
	else:
		if abs(prop) < 180:
			duty = round(abs(prop)/6)+70
			PWM.set_duty_cycle("P8_13", 0)
			PWM.set_duty_cycle("P8_19", duty)
		else:
			duty = round((360-abs(prop))/6)+70
			PWM.set_duty_cycle("P8_19", 0)
			PWM.set_duty_cycle("P8_13", duty)
			 
		

##############################################################################

PWM.start("P8_13", 0)
PWM.start("P8_19", 0)
ADC.setup()
UART.setup("UART4")

ser = serial.Serial(port = "/dev/ttyO4", baudrate=115200, 
parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
bytesize=serial.EIGHTBITS, timeout=0, xonxoff=0, rtscts=0)

read_pin = 'P9_40'
ByteToSend = "\xCF"
Data = ""

if ser.isOpen():
	while True:
		ser.write(ByteToSend)
		while ser.inWaiting() !=31: 
			a=0

		data = ser.read(31)
		angle = ANG_read(read_pin)
		good = check_sum(data)

		if good == 1:
			roll = imu_convert(bit_check(data[1:5]))
			target = round(((roll*51.42857143)+167.1428571), 
1)
			set = motor_set(target, roll)
			print ('%f\t%f' % (target, roll))
