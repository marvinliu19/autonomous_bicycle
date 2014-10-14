# Reads angle from potentiometer and applies exponential filter
import Adafruit_BBIO.ADC as ADC
import time 

pin = 'P9_40'
ADC.setup()
SMOOTH = 0.8 # Closer to 1 means less smoothing

# Reads a voltage from the potentiometer between 0 and 1
# Multiplies it by 360 to get an angle
def read_angle(sensor_pin):
	return ADC.read(sensor_pin)*360

# Averages the first four values to get a starting
# value for the exponential filters
def get_initial_value(sensor_pin):
	pt1 = read_angle(sensor_pin)
	pt2 = read_angle(sensor_pin)
	pt3 = read_angle(sensor_pin)
	pt4 = read_angle(sensor_pin)
	return ((pt1 + pt2 + pt3 + pt4)/4)

# Timer for testing
init_time = time.time()
elasped_time = 0

# Sets the initial value in the exponential filter
cur_data = get_initial_value(pin)
data_points = 1
# Gathers 5 seconds of data
while data_points < 1001:
	elasped_time = time.time() - init_time
	# Exponential smoothing
	cur_data = SMOOTH*read_angle(pin) + (1-SMOOTH)*cur_data
	print "%.6f %f"%(elasped_time, cur_data)
	data_points = data_points + 1