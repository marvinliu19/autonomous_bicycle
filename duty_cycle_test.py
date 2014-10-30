import Adafruit_BBIO.PWM as PWM

# Output pins to the motor
direction = "P8_19"
duty_cycle = "P8_13"

# Constants
FORWARD = 100
REVERSE = 0

if __name__ == '__main__':    
  target = input('enter duty: ')
  PWM.start(direction, FORWARD)
  PWM.start(duty_cycle, target)



