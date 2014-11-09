# Module for communication with the potentiometer
import Adafruit_BBIO.ADC as ADC

# Class that holds the current potentiometer data
# Method get_steer_angle() returns the current steer angle
class Potentiometer:
	def __init__(self,pin):
		self.SMOOTH = 0.8 # Closer to 1 means less smoothing
		self.pin = pin
		self.data = get_initial_value()
		ADC.setup()

	# Averages four readings to get starting value for the exponential filter
	# @param pin: GPIO pin for the potentiometer
	# Return: average of four potentiometer readings
	def get_initial_value():
		pt1 = read_angle()
		pt2 = read_angle()
		pt3 = read_angle()
		pt4 = read_angle()
		return ((pt1 + pt2 + pt3 + pt4)/4)

	# Reads a voltage from the potentiometer between 0 and 1
	# Multiplies it by 360 to get an angle
	def read_angle():
		return ADC.read(self.pin)*360

	# Returns the current steer angle with exponential filtering	
	def get_steer_angle(self): 
		self.data = self.SMOOTH*read_angle() + (1-self.SMOOTH)*self.data
		return self.data

