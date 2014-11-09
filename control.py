# Main control for the robotic bicycle
import Adafruit_BBIO.UART as UART
import serial
import time
import math
import imu 
import potentiometer as Pot
import pid 
###############################   Constants   ##################################

# Control Constants
PERIOD = 0.1 		# Seconds per calculation cycle

# Potentiometer Constants
POT_PIN = 'P9_40'	# Input pin on BeagleBone Black for potentiometer

# Motor Constants
DIR_PIN = "P8_19"
DUTY_PIN = "P8_13"
KP = 0.15
KI = 0
KD = 0.001
QMAX = 982

############################   Initialization   ################################

# Initialize serial port for the IMU
UART.setup("UART4")
imu_serial_port = serial.Serial(port = "/dev/ttyO4", baudrate=115200, 
	parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
	bytesize=serial.EIGHTBITS, timeout=0, xonxoff=0, rtscts=0)

# Initialize the potentiometer
pot = Pot.Potentiometer(POT_PIN)

# Initialize the motor
motor = pid.MotorController(pot, DIR_PIN, DUTY_PIN, KP, KI, KD, QMAX)

################################################################################

def control_cycle(start_time):
	lean_angle = imu.get_roll_angle(imu_serial_port)
	steer_angle = pot.get_angle()
	
	# Output to motor
	target_angle = math.degrees(lean_angle) + 180
	motor.control_motor(target_angle, time.time())			
	
	# Calculate left over time to wait
	extra_time = PERIOD - (time.time() - start_time)
	time.sleep(extra_time)

while True:
	control_cycle(time.time())

	
	


