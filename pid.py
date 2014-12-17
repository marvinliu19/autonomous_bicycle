import Adafruit_BBIO.PWM as PWM
import time

# A proportional-integral-derivative controller for the steering motor
class MotorController:
  # Creates a new MotorController object
  # @param: pot - a Potentiometer object used to get the current steer angle
  # @param: dir_pin - output pin on BeagleBone that controls motor direction
  # @param: duty_pin - output pin on BeagleBone that controls duty cycle
  # @param: kp - KP constant in the PID controller
  # @param: ki - KI constant in the PID controller
  # @param: kd - KD constant in the PID controller
  # @param: qmax - the maximum q (wind-up) allowed in the PID controller
  # @return: MotorController object set in forward direction and duty cycle = 0
  def __init__(self, pot, dir_pin, duty_pin, kp, ki, kd, qmax):
    self.REVERSE = 0
    self.FORWARD = 100
    self.pot = pot
    self.dir_pin = dir_pin
    self.duty_pin = duty_pin
    self.kp = kp
    self.ki = ki
    self.kd = kd
    self.qmax = qmax
    self.q = 0
    self.duty = 0
    self.counter = 0
    self.prev_error = 0

    PWM.start(self.dir_pin, 100, 20000, 0)
    PWM.start(self.duty_pin, 0, 20000, 0)

  # Sets the motor in the direction of shortest path to correct the angle error
  # Changes the angle error to be in the range [0,180)
  # This guarentees that the motor does not turn the long way around to reach a
  # target angle.
  # Postcondition: returns a value in the range [0,180)
  # @param: angle_error - the difference between target angle and current angle
  # @return: the new angle error after motor direction is changed
  def set_dir_angle_error(self, angle_error):
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

  # Prevents windup in the integral controller
  def anti_windup(self):
    self.counter = self.counter + 1
    if self.counter == 3:
      self.q = 0
      self.counter = 0
  
  # Calculates a output duty cycle using the PID control 
  # Can return numbers > 100 or < 0
  # @param: e - the error
  # @param: del_e - the change in error since the last cycle
  # @param: t - the start time of the cycle
  # @return: an output duty cycle 
  def calc_motor_output(self, e, del_e, t):
    return self.kp*(e+(self.ki*self.q)+(self.kd*(del_e/(time.time()-t))))
  
  # Sets the duty cycle and direction of the motor to reach the target velocity
  # @param: target_velocity - the velocity the controller is trying to reach
  # @param: start_time - the time when the function is called
  def control_motor(self, target_velocity, start_time):
    vel_error = target_velocity - self.pot.get_velocity()
    delta_error = abs(vel_error - self.prev_error)
     
    self.q = min(self.q + (time.time()-start_time)*vel_error, self.qmax)
    self.anti_windup()
  
    output_duty = min(self.calc_motor_output(vel_error,delta_error,start_time),100)
    self.print_state(output_duty)
    
    #Update variables
    self.duty = output_duty
    self.prev_error = vel_error
  
    PWM.set_duty_cycle(self.duty_pin, output_duty)
  
  # Prints the current duty cycle and the angle of the steering motor
  # @param: output_duty - the output duty cycle calculated
  def print_state(self, output_duty):
    print "Output duty: %f"%(output_duty)
    print"Position: %f\tVelocity: %f"%(self.pot.get_angle(), self.pot.get_velocity())