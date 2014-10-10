import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time
from multiprocessing import Process

# Input pin from the potentiometer
potentiometer = 'P9_40'
ADC.setup()

# Output pins to the motor
direction = "P8_19"
duty_cycle = "P8_13"

# Constants
FORWARD = 100
REVERSE = 0

# Stablizes the motor at the target angle
def control_motor(target_angle):
	PWM.start(direction, FORWARD)
	PWM.start(duty_cycle, 0)
    current_direction = FORWARD
	while True:
        # Difference between target angle and current angle
		angle_error = target_angle - (ADC.read(potentiometer)*360)
        proportional_duty = angle_error/3.6 # /360 * 100

		if (angle_error < 0 and current_direction == FORWARD):
            PWM.set_duty_cycle(direction, REVERSE)
            PWM.set_duty_cycle(duty_cycle, proportional_duty)
            current_direction = REVERSE
        
        elif (angle_error > 0 and current_direction == REVERSE):
            PWM.set_duty_cycle(direction, FORWARD)
            PWM.set_duty_cycle(duty_cycle, proportional_duty)
            current_direction = FORWARD
        
        else:
            PWM.set_duty_cycle(duty_cycle, proportional_duty)8

control_motor(180)	


