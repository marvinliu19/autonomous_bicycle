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
KP = 0.15
KI = 0
QMAX = 982
KD = 0.001

# Variables
q = 0
duty = 0
counter = 0
prev_error = 0

# Starts the motor in a forward direction with a duty cycle of 0
def motor_start():
  PWM.start(direction, FORWARD)
  PWM.start(duty_cycle, 0)

def control_motor(target_angle, start_time):
  global duty
  global q
  global counter
  global prev_error

  output_duty = 0

  angle_error = target_angle - (ADC.read(potentiometer)*360)
  delta_error = abs(angle_error - prev_error)

  if angle_error < 0:
    if abs(angle_error) < 180:
      PWM.set_duty_cycle(direction, REVERSE)
      angle_error = abs(angle_error)   
    else:
      PWM.set_duty_cycle(direction, FORWARD)
      angle_error = abs(angle_error) - 180
  else:
    if abs(angle_error) < 180:
      PWM.set_duty_cycle(direction, FORWARD)
    else:
      PWM.set_duty_cycle(direction, REVERSE)
      angle_error = angle_error - 180

  q = min(q + (time.time()-start_time)*angle_error, QMAX)
  counter = counter + 1
  if counter == 3:
    q = 0
    counter = 0

  pid_output = KP*(angle_error + (KI*q) + (KD*(delta_error/(time.time()-start_time))))
  output_duty = min(pid_output, 100)
  print "Output duty: %f"%(output_duty)
  
  #Update variables
  duty = output_duty
  prev_error = angle_error

  PWM.set_duty_cycle(duty_cycle, output_duty)
  
  print"%f"%(ADC.read(potentiometer)*360)
  

if __name__ == '__main__':    
  motor_start()
  while True:
    control_motor(90, time.time())



