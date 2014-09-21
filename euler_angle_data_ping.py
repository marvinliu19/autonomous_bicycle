#Written by Marvin Liu
#Uses pinging to continuously print euler angle data
#import Adafruit_BBIO.UART as UART
import serial
import time
import struct 
from multiprocessing import Process, Queue

#UART.setup("UART4")

# Initialize serial port
# Use port /dev/ttyUSB0 for serial USB connection on laptop
# Use port /dev/ttyO4 for BeagleBone Black
ser = serial.Serial(port = "/dev/ttyUSB0", baudrate=115200, 
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

def imu_convert(a):
	d = struct.unpack('!f', a.decode('hex'))[0]
	return d

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

# Puts data from IMU onto queue as a tuple of (time,data)
# Precondition: queue is from multiprocessing.Queue
def print_data(serial_port):
	initial_time = time.time()
	if serial_port.isOpen():
		while True:
			ser.write("\xCF")
			if (serial_port.inWaiting() < 31):
				continue
			data = serial_port.read(31)
			if valid_check_sum(data):
				time_elasped = time.time()-initial_time
				roll = imu_convert(bit_check(data[1:5]))
				pitch = imu_convert(bit_check(data[5:9]))
				yaw = imu_convert(bit_check(data[9:13]))
				print('Time: %f Roll: %f  Pitch: %f  Yaw: %f'%(time_elasped,roll,pitch,yaw))

# Puts data from IMU onto queue as a tuple of (time,data)
# Precondition: queue is from multiprocessing.Queue
def write_data(serial_port, queue):
	initial_time = time.time()
	if serial_port.isOpen():
		print "Serial Status: Open"
		while True:
			#ser.write("\xCF")
			if (serial_port.inWaiting() < 31):
				print "Insufficient Data"
				time.sleep(0.5)
			data = serial_port.read(31)
			if valid_check_sum(data):
				#time_data_tuple = ((time.time()-initial_time),data)
				#queue.put(time_data_tuple)
				
				roll = imu_convert(bit_check(data[1:5]))
				pitch = imu_convert(bit_check(data[5:9]))
				yaw = imu_convert(bit_check(data[9:13]))
				print('Time: %f Roll: %f  Pitch: %f  Yaw: %f'%((time.time()-initial_time),roll,pitch,yaw))

# Gets (time,data) tuple from queue and print to screen
# Precondition: queue is from multiprocessing.Queue
def read_data(queue):
	while True:
		if not queue.empty():
			data_tuple = queue.get()
			time_put = data_tuple[0]
			data = data_tuple[1]
			
			roll = imu_convert(bit_check(data[1:5]))
			pitch = imu_convert(bit_check(data[5:9]))
			yaw = imu_convert(bit_check(data[9:13]))
			print('Time:%f  Roll:%f  Pitch:%f  Yaw:%f'%(time_put,roll,pitch,yaw))

print_data(ser)

		
	