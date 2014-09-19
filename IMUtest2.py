#import Adafruit_BBIO.UART as UART
import serial
import time

#UART.setup("UART4")

ser = serial.Serial(port = "/dev/ttyUSB0", baudrate=115200, 
parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
bytesize=serial.EIGHTBITS, timeout=0, xonxoff=0, rtscts=0)

if ser.isOpen():
	print "Serial Status: Open"
	ByteToSend = "\xC2"
	ser.write(ByteToSend)
	time.sleep(2)
	RecievedData = ""
	header = ""
	xaccel = ""
	yaccel = ""
	zaccel = ""
	xangrate = ""
	yangrate = ""
	zangrate = ""
	timer = ""
	checksum = ""
	while ser.inWaiting() > 0:
		RecievedData = ser.read(31)
		header = RecievedData[0:1]
		xaccel = RecievedData[1:5]
		yaccel = RecievedData[5:9]
		zaccel = RecievedData[9:13]
		xangrate = RecievedData[13:17]
		yangrate = RecievedData[17:21]
		zangrate = RecievedData[21:25]
		timer = RecievedData[25:29]
		checksum = RecievedData[29:31]
	print "\nHeader"
	print " ".join(hex(ord(n)) for n in header)
	print "\nX acceleration"
	print " ".join(hex(ord(n)) for n in xaccel)
	print "\nY acceleration"
	print " ".join(hex(ord(n)) for n in yaccel)
	print "\nZ acceleration"
	print " ".join(hex(ord(n)) for n in zaccel)
	print "\nX angular rate"
	print " ".join(hex(ord(n)) for n in xangrate)
	print "\nY angular rate"
	print " ".join(hex(ord(n)) for n in yangrate)
	print "\nZ angular rate"
	print " ".join(hex(ord(n)) for n in zangrate)
	#print " ".join(hex(ord(n)) for n in RecievedData)
ser.close
print "Serial Status: Closed"
