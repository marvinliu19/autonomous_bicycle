# Module for communication with the IMU
import struct 

# Helper function to process raw data from the IMU
# @param: a - raw data to be converted
# @return: processed data to be sent to imu_convert
def bit_check(a):
	c = ""
	for x in range(0, len(a)):
		b = hex(ord(a[x])).lstrip("0x") or "0"
		if len(b) != 2:
			b = '0'+b
		c = c+b
	return c 

# Converts 4 bytes into a floating point number
# @param: a - data from bit_check to be converted
# @return: float representation of bytes
def imu_convert(a):
	data = struct.unpack('!f', a.decode('hex'))[0]
	return data

# Checks if the IMU data has a valid check sum
# Precondition: data has length 31
# @param data: a string of data from the IMU
# Return: True if valid, False if invalid
def valid_check_sum(data):
	b = 0
	for x in range(0, 29):
		b = ord(data[x])+b
	c = hex(ord(data[29])).lstrip("0x") or "0"
	d = hex(ord(data[30])).lstrip("0x") or "0"
	e = int(c+d, 16)
	return (e==b)

# Gets the current roll angle and angular rates of the IMU
# @param serial_port: serial port the IMU is connected to
# Return: roll angle from -pi to pi and angular rates in x, y, and z directions
def get_roll_angle_ang_rate(serial_port):
	while True:
		serial_port.write("\xCF")
		while (serial_port.inWaiting() < 31):
			pass
		data = serial_port.read(31)
		if valid_check_sum(data):
			pitch = imu_convert(bit_check(data[5:9]))
			ang_rate_x = imu_convert(bit_check(data[13:17]))
			ang_rate_y = imu_convert(bit_check(data[17:21]))
			ang_rate_z = imu_convert(bit_check(data[21:25]))
			return (pitch, ang_rate_x, ang_rate_y, ang_rate_z)
