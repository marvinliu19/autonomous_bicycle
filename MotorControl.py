import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time

read_pin = 'P9_40'

ADC.setup()
PWM.start("P8_13", 100)

print('Reading\t\tAngle')
count = 0

while count < 60:
	reading = ADC.read(read_pin)
	angle = reading * 360
	print('%f\t%f' % (reading, angle))
	time.sleep(.25)
	count = count + 1

PWM.stop("P9_14")
PWM.cleanup()

