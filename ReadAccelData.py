#import Adafruit_BBIO.UART as UART
import serial
import time
import struct 

#UART.setup("UART4")

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

def check_sum(a):
	b = 0
	for x in range(0, 29):
		b = ord(a[x])+b

	c = hex(ord(a[29])).lstrip("0x") or "0"
	d = hex(ord(a[30])).lstrip("0x") or "0"
	e = int(c+d, 16)
	if e == b:
		f = 1
	else:
		f = 0

	return f

ByteToSend = "\xCF"
Data = ""
holder=[]
time_cur=time.time()
time_init=time.time()
dif = time_cur-time_init

if ser.isOpen():
	while dif < 10:
		ser.write(ByteToSend)
		while ser.inWaiting() != 31:
			a = 0 
		data = ser.read(31)
		time_cur = time.time()	
		dif = time_cur-time_init
		good = check_sum(data)
		if good == 1:
			Data = Data+data
			holder.append(dif)

up=0
for x in range(0, (len(Data)/31)):
	roll = imu_convert(bit_check(Data[(1+up):(5+up)]))
	pitch = imu_convert(bit_check(Data[(5+up):(9+up)]))
	yaw = imu_convert(bit_check(Data[(9+up):(13+up)]))
	print ('%f  %f  %f  %f' % (holder[x], roll, pitch, yaw))
	up=up+31
	


############################################################################

	#data = bit_check(Data)
	#roll = imu_convert(bit_check(Data[1:5]))
	#pitch = imu_convert(bit_check(Data[5:9]))
	#yaw = imu_convert(bit_check(Data[9:13]))
	#xang = imu_convert(bit_check(Data[13:17]))
	#yang = imu_convert(bit_check(Data[17:21]))
	#zang = imu_convert(bit_check(Data[21:25]))
	#timer = imu_convert(bit_check(Data[25:29]))
	#checksum = bit_check(Data[29:31])
	
	#print "\nData Packet"
	#print "".join(hex(ord(n)).lstrip("0x") for n in Data)
	#print data

#print "\nRoll"
#print roll
#print "\nPitch"
#print pitch
#print "\nYaw"
#print yaw
#print "\nX angular rate"
#print xang
#print "\nY angular rate"
#print yang
#print "\nZ angular rate"
#print zang	
#print "\nTimer"
#print timer

#good = check_sum(Data)
#print "\ncheck sum check"
#print good
		
ser.close
