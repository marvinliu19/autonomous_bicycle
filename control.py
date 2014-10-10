# Main control for the robotic bicycle

#import Adafruit_BBIO.UART as UART
#import Adafruit_BBIO.ADC as ADC
import serial
import time
import struct 
from multiprocessing import Process, Queue

# Constants
PERIOD = 0.1 		# Seconds per calculation cycle
PIN = 'P9_40'	# Input pin on BeagleBone Black for potentiometer

# Global variables
#ser = serial.Serial(port = "/dev/ttyO4", baudrate=115200, 
					#parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
					#bytesize=serial.EIGHTBITS, timeout=0, xonxoff=0, rtscts=0)
lean_queue = Queue()
steer_queue = Queue()

###############################################################################

# IMU Helper Functions
def bit_check(a):
	c = ""
	for x in range(0, len(a)):
		b = hex(ord(a[x])).lstrip("0x") or "0"
		if len(b) != 2:
			b = '0'+b
		c = c+b
	return c 

# Converts 4 bytes into a floating point number
# Precondition: raw is 4 bytes
# Postcondition: Returns a float
def imu_convert(raw):
	data = struct.unpack('!f', raw.decode('hex'))[0]
	return data

# Checks if data has a valid check sum
# Precondition: data is a string containing 31 bytes
# Postcondition: Returns True if checksum valid, False if invalid
def valid_check_sum(data):
	b = 0
	for x in range(0, 29):
		b = ord(data[x])+b

	c = hex(ord(data[29])).lstrip("0x") or "0"
	d = hex(ord(data[30])).lstrip("0x") or "0"
	e = int(c+d, 16)
	return (e==b)

###############################################################################

# Calculates voltage given lean angle and steer angle
# Precondition: Lean is the range -pi-pi and steer is in the range 0-360
# Postcondition: Return voltage in range 0-3.3V
def voltage_output(lean, steer):
	return 0

# Puts lean angle data from IMU onto a queue
def enqueue_lean(serial_port, queue):
	while True:
		serial_port.write("\xCF")
		while (serial_port.inWaiting() < 31):
			a = 0
		data = serial_port.read(31)
		if valid_check_sum(data):
			roll = imu_convert(bit_check(data[1:5]))
			queue.put(roll)

# Puts data from potentiometer onto a queue
def enqueue_steer(sensor_pin, queue):
	return 0	

def factorial(n):
	if n == 1: 
		return 1
	else:
		return n * factorial(n-1)

def control_cycle(start_time):
	# Do stuff
	x = factorial(20) # Temporary function call
	
	# Calculate left over time to wait
	extra_time = PERIOD - (time.time() - start_time)
	time.sleep(extra_time)

# Print the time that each cycle took to execute
count = 0
while count < 200:
	start = time.time()
	control_cycle(start)
	end = time.time()
	print "%f"%(end - start)
	count = count + 1

	
	


