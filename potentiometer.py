# Module for communication with the potentiometer
import Adafruit_BBIO.ADC as ADC

ADC.setup()
SMOOTH = 0.8 # Closer to 1 means less smoothing

# Reads a voltage from the potentiometer between 0 and 1
# Multiplies it by 360 to get an angle
def read_angle(pin):
	return ADC.read(pin)*360

# Averages four readings to get starting value for the exponential filter
# @param pin: GPIO pin for the potentiometer
# Return: average of four potentiometer readings
def get_initial_value(pin):
	pt1 = read_angle(pin)
	pt2 = read_angle(pin)
	pt3 = read_angle(pin)
	pt4 = read_angle(pin)
	return ((pt1 + pt2 + pt3 + pt4)/4)

# Class that holds the current potentiometer data
# Method get_steer_angle() returns the current steer angle
class Potentiometer:
	def __init__(self,pin):
		self.data = get_initial_value(pin)
		self.pin = pin
	def get_steer_angle(self): 
		self.data = SMOOTH*read_angle(self.pin) + (1-SMOOTH)*self.data
		return self.data

# Testing
if __name__ == '__main__':
	pot = Potentiometer('P9_40')
	for x in range(0,1000)
		print "%f"%(pot.get_steer_angle())
		