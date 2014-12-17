# Module for communication with the potentiometer
import Adafruit_BBIO.ADC as ADC
import math

# Averages four readings to get starting value for the exponential filter
# @param: pin - GPIO pin for the potentiometer
# @return: initial value for exponential filter
def get_initial_value(pin):
	pt1 = read_angle(pin)
	pt2 = read_angle(pin)
	pt3 = read_angle(pin)
	pt4 = read_angle(pin)
	return ((pt1 + pt2 + pt3 + pt4)/4)

# Reads the current angle of the potentiometer
# @param: pin - GPIO pin for the potentiometer
# @return: current angle of the potentiometer
def read_angle(pin):
	return ADC.read(pin)*360

# Class that holds the current potentiometer data
class Potentiometer:
	# Creates a new Potentiometer object
	# @param: pin - GPIO pin for the potentiometer
	# @return: potentiometer with exponential filter smoothing constant of 0.8
	def __init__(self,pos_pin, vel_pin):
		ADC.setup()
		self.SMOOTH = 0.8
		self.pos_pin = pos_pin
		self.vel_pin = vel_pin
		self.data = get_initial_value(self.pin)
		
	# Reads the current angle of the potentiometer
	# @return: current angle of the potentiometer
	def get_angle(self):
		return ADC.read(self.pos_pin) * 2 * math.pi

	# Reads the current angular velocity of the potentiometer
	# @return: current angular velocity of the potentiometer
	# Resting value: 0.896 / 1.8
	def get_velocity(self):
		return (ADC.read(self.vel_pin) - (0.896 / 1.8))

	# Reads the current angle of the potentiometer with exponential filtering
	# Reduces the noise caused by the analog to digital conversion
	# @return: exponentially filtered angle of the potentiometer
	def get_steer_angle(self): 
		self.data = self.SMOOTH*self.get_angle() + (1-self.SMOOTH)*self.data
		return self.data

