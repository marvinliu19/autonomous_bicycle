# Module for communication with the IMU
import struct 

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
# @param data: a string containing 31 bytes
# Return: True if valid, False if invalid
def valid_check_sum(data):
	b = 0
	for x in range(0, 29):
		b = ord(data[x])+b

	c = hex(ord(data[29])).lstrip("0x") or "0"
	d = hex(ord(data[30])).lstrip("0x") or "0"
	e = int(c+d, 16)
	return (e==b)

# Gets the current roll angle of the IMU
# @param serial_port: serial port the IMU is connected to
# Return: roll angle value between -pi and pi 
def get_roll_angle(serial_port):
	while True:
		serial_port.write("\xCF")
		while (serial_port.inWaiting() < 31):
			pass
		data = serial_port.read(31)
		if valid_check_sum(data):
			return imu_convert(bit_check(data[1:5]))
