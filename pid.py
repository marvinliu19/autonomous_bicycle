import Adafruit_BBIO.PWM as PWM
import time

class MotorController:
  def __init__(self, pot, kp, ki, kd, qmax):
    self.REVERSE = 0
    self.FORWARD = 100
    self.pot = pot
    self.dir_pin = "P8_19"
    self.duty_pin = "P9_13"
    self.kp = kp
    self.ki = ki
    self.kd = kd
    self.qmax = qmax
    self.q = 0
    self.duty = 0
    self.counter = 0
    self.prev_error = 0

    PWM.start(self.dir_pin, 100)
    PWM.start(self.duty_pin, 0)

  def set_dir_angle_error(angle_error):
    if angle_error < 0:
      if abs(angle_error) < 180:
        PWM.set_duty_cycle(self.dir_pin, self.REVERSE)
        return abs(angle_error)   
      else:
        PWM.set_duty_cycle(self.dir_pin, self.FORWARD)
        return abs(angle_error) - 180
    else:
      if abs(angle_error) < 180:
        PWM.set_duty_cycle(self.dir_pin, self.FORWARD)
        return angle_error
      else:
        PWM.set_duty_cycle(self.dir_pin, self.REVERSE)
        return angle_error - 180

  def anti_windup(self):
    self.counter = self.counter + 1
    if self.counter == 3:
      self.q = 0
      self.counter = 0
  
  def calc_motor_output(e, del_e, t):
    return self.KP*(e+(self.KI*self.q)+(self.KD*(del_e/(time.time()-t))))
  
  def control_motor(target_angle, start_time):
    angle_error = target_angle - self.pot.read_angle()
    delta_error = abs(angle_error - self.prev_error)
    angle_error = set_dir_angle_error(angle_error)
    
    self.q = min(self.q + (time.time()-start_time)*angle_error, self.qmax)
    anti_windup()
  
    output_duty = min(calc_motor_output(angle_error,delta_error,start_time),100)
    print_state(pot, output_duty)
    
    #Update variables
    self.duty = output_duty
    self.prev_error = angle_error
  
    PWM.set_duty_cycle(self.duty_pin, output_duty)
  
  def print_state(self, output_duty):
    print "Output duty: %f"%(output_duty)
    print"%f"%(self.pot.read_angle()*360)