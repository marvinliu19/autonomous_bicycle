#Written by Marvin Liu

#import Adafruit_BBIO.UART as UART
import serial
import time
import struct 
from multiprocessing import Process, Queue

#UART.setup("UART4")

#Use port /dev/ttyUSB0 for laptop
#Use port /dev/ttyO4 for BeagleBone Black
ser = serial.Serial(port = "/dev/ttyUSB0", baudrate=115200, 
parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
bytesize=serial.EIGHTBITS, timeout=0, xonxoff=0, rtscts=0)

#Sets the IMU to continuously send Euler Angle and Angular Rate Data
def set_continuous_euler_ang():
	command = "\xC4"
	confirm1 = "\xC1"
	confirm2 = "\x29"
	euler_ang = "\xCF"
	
	ser.write(command)
	ser.write(confirm1)
	ser.write(confirm2)
	ser.write(euler_ang)	

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

#Checks if data packet has a valid check sum
def valid_check_sum(a):
	b = 0
	for x in range(0, 29):
		b = ord(a[x])+b

	c = hex(ord(a[29])).lstrip("0x") or "0"
	d = hex(ord(a[30])).lstrip("0x") or "0"
	e = int(c+d, 16)
	return (e==b)

def write_data(queue):
	initial_time = time.time()
	if ser.isOpen():
		print "Serial Status: Open"
		while True:
			while ser.inWaiting() < 31:
				a = 0
			data = ser.read(31)
			if valid_check_sum(data):
				time_data_tuple = ((time.time()-initial_time),data)
				queue.put(time_data_tuple)

def read_data(queue):
	while True:
		if not queue.empty():
			data_tuple = queue.get()
			time = data_tuple[0]
			data = data_tuple[1]
			
			roll = imu_convert(bit_check(data[1:5]))
			pitch = imu_convert(bit_check(data[5:9]))
			yaw = imu_convert(bit_check(data[9:13]))
			print('Time:%f  Roll:%f  Pitch:%f  Yaw:%f'%(time,roll,pitch,yaw))

#Create a queue that will hold (time,data) tuples
queue = Queue()

#Create a seperate process to read the data
data_reader = Process(target=read_data, args=((queue),))
data_reader.daemon = True
data_reader.start()        

#Set the IMU to continuously send data about Euler Angles and Angular Rate
set_continuous_euler_ang()

#Write the output from the IMU onto the queue
write_data(queue)



############################################################################
	#xang = imu_convert(bit_check(data[13:17]))
	#yang = imu_convert(bit_check(data[17:21]))
	#zang = imu_convert(bit_check(data[21:25]))
		
	