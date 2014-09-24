# Written by Marvin Liu 
# Polls IMU continuously for euler angle data

import Adafruit_BBIO.UART as UART
import serial
import time
import struct 
from multiprocessing import Process, Queue

UART.setup("UART4")

# Initialize serial port
ser = serial.Serial(port = "/dev/ttyO4", baudrate=115200, 
parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
bytesize=serial.EIGHTBITS, timeout=0, xonxoff=0, rtscts=0)

def bit_check(a):
	c = ""
	for x in range(0, len(a)):
		b = hex(ord(a[x])).lstrip("0x") or "0"
		if len(b) != 2:
			b = '0'+b
		c = c+b
	return c 

# Converts 4 bytes into a floating point number
def imu_convert(a):
	data = struct.unpack('!f', a.decode('hex'))[0]
	return data

# Checks if data has a valid check sum
# Precondition: data is a string containing 31 bytes
# Return: True if valid, False if invalid
def valid_check_sum(data):
	b = 0
	for x in range(0, 29):
		b = ord(data[x])+b

	c = hex(ord(data[29])).lstrip("0x") or "0"
	d = hex(ord(data[30])).lstrip("0x") or "0"
	e = int(c+d, 16)
	return (e==b)

# Puts data from IMU onto queue as a tuple of (time_elasped,data)
# Precondition: queue is from multiprocessing.Queue
def write_data(serial_port, queue):
	initial_time = time.time()
	while True:
		ser.write("\xCF")
		if (serial_port.inWaiting() < 31):
			continue
		data = serial_port.read(31)
		
		if valid_check_sum(data):
			time_elasped = time.time()-initial_time
			queue.put((time_elasped,data))
		else:
			print "Invalid Data"
		
# Gets (time,data) tuple from queue and print to screen
# Precondition: queue is from multiprocessing.Queue
def read_data(queue):
	while True:
		data_tuple = queue.get()
		time_elasped = data_tuple[0]
		data = data_tuple[1]
		# roll = bit_check(data[1:5])
		roll = imu_convert(bit_check(data[1:5]))
		pitch = imu_convert(bit_check(data[5:9]))
		yaw = imu_convert(bit_check(data[9:13]))
		print('Time: %f  Roll: %s  Pitch: %f  Yaw: %f'%(time_elasped,roll,pitch,yaw))

if ser.isOpen():
	#Create a queue that will hold (time,data) tuples
	queue = Queue()
	#Create a seperate process to read the data
	data_reader = Process(target=read_data, args=((queue),))
	data_reader.daemon = True
	data_reader.start()        
	
	#Write the output from the IMU onto the queue
	write_data(ser, queue)

else:
	print "Error: Serial port not open"