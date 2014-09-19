import Adafruit_BBIO.ADC as ADC
import time 
import numpy as np

def ANG_read(a,n):
	y=time.time()
	b=np.ones(n)
	for x in range(0, n):
		b[x]=ADC.read(a)*360

	c=round(sum(b)/n,1)
	x=time.time()
	dif=x-y
	return (c,dif)

def avgtest(a,n):
	z=time.time()
	b=np.zeros(n)
	for x in range(0, n):
		b[x]=ADC.read(a)*360	

	avg=round(sum(b)/n, 1)
	y=time.time()
	dif=y-z
	print ('%.1f\t%f' % (avg, dif))	

sensor_pin = 'P9_40'
num_cycles=10
ADC.setup()
avgtest(sensor_pin, num_cycles)

#print('Angle\t\tTime')
#count = 0

#while count<10:
#	(angle, dif) = ANG_read(sensor_pin,num_cycles)
#	print('%f\t%f' % (angle, dif))
#	count += 1
