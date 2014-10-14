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

# PWM.start(direction_pin, 100)
# PWM.start(duty_cycle_pin, 100)

change_direction_delay = 2

# Reverse the direction every t seconds
def control_motor(t):
	# Start PWM signals
	PWM.start(direction_pin, 100)
	PWM.start(duty_cycle_pin, 50)
	while True:
		time.sleep(t)
		PWM.set_duty_cycle(direction_pin, 0)
		time.sleep(t)
		PWM.set_duty_cycle(direction_pin, 100)
	
motor_control = Process(target=control_motor, args=(change_direction_delay,))
motor_control.daemon = True
motor_control.start()

count = 0
while count < 2000:
	print"%f"%(ADC.read(pot_pin)*360)
 	count = count + 1

