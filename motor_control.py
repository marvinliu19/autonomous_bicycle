import Adafruit_BBIO.PWM as PWM
import Adafruit_BBIO.ADC as ADC
import time

# Input pin from the potentiometer
potentiometer = 'P9_40'
ADC.setup()

# Output pins to the motor
direction = "P8_19"
duty_cycle = "P8_13"

# Constants
FORWARD = 100
REVERSE = 0

def motor_start():
  PWM.start(direction, FORWARD)
  PWM.start(duty_cycle, 0)
  current_direction = FORWARD

# Stablizes the motor at the target angle
def control_motor(target_angle):
  while True:
    # Difference between target angle and current angle
    angle_error = target_angle - (ADC.read(potentiometer)*360)
    proportional_duty = 0
    if angle_error < 0:
      if abs(angle_error) < 180:
        PWM.set_duty_cycle(direction, REVERSE)
        proportional_duty = abs(angle_error)/180*99 + 1   
      else:
        PWM.set_duty_cycle(direction, FORWARD)
        proportional_duty = (abs(angle_error) - 180)/180*99 + 1
    else:
      if abs(angle_error) < 180:
        PWM.set_duty_cycle(direction, FORWARD)
        proportional_duty = abs(angle_error)/180*99 + 1   
      else:
        PWM.set_duty_cycle(direction, REVERSE)
        proportional_duty = (abs(angle_error) - 180)/180*99 + 1
    
    PWM.set_duty_cycle(duty_cycle, proportional_duty)
    print"%f"%(ADC.read(potentiometer)*360)

if __name__ == '__main__':    
    motor_start()
    control_motor(90)



