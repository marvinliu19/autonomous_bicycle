import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time
from multiprocessing import Process

# Input pin from the potentiometer
pot_pin = 'P9_40'
ADC.setup()

# Output pins to the H bridge
direction_pin = "P8_19"
duty_cycle_pin = "P8_13"

PWM.start(direction_pin, 100)
PWM.start(duty_cycle_pin, 25)

count = 0
while count < 2000:
	print"%f"%(ADC.read(pot_pin)*360)
 	count = count + 1

