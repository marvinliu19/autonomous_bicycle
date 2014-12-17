# Main controller for the autonomous bicycle using a BeagleBone Black
import Adafruit_BBIO.UART as UART
import Adafruit_BBIO.PWM as PWM
import serial
import time
import math
import imu 
import potentiometer as Pot
import pid 

# Seconds per calculation cycle
PERIOD = 0.1
# Potentiometer pins on BeagleBone Black
VELOCITY_PIN ='P9_39'
POS_PIN ='P9_40'

# Motor Constants
MOTOR_PIN = "P9_16"	#PWM1B
DIR_PIN = "P8_19" 	#PWM2A
DUTY_PIN = "P8_13" 	#PWM2B
KP = 0.15
KI = 0
KD = 0.001
QMAX = 982

# Initialize serial port for the IMU
UART.setup("UART4")
imu_serial_port = serial.Serial(port = "/dev/ttyO4", baudrate=115200, 
	parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
	bytesize=serial.EIGHTBITS, timeout=0, xonxoff=0, rtscts=0)

# Initialize the potentiometer and motor
pot = Pot.Potentiometer(POS_PIN, VELOCITY_PIN)
motor = pid.MotorController(pot, DIR_PIN, DUTY_PIN, KP, KI, KD, QMAX)

# Start the motor hub
PWM.start(MOTOR_PIN, 50)

# Calculates the target steering angle to stabilize the bicycle
# @param: lean_angle - the lean angle of the bicycle
# @param: lean_velocity - the rate at which the bicycle is leaning
# @param: steer_angle - the angle of the steering wheel of the bicycle
# @return: the angular velocity the steering wheel must be turning at to reach 
#	stability
def calculate(lean_angle, lean_velocity, steer_angle):
	k1 = -4.8174
	k2 = -1.0151
	k3 = 5.5671
	return -(k1*lean_angle + k2*lean_velocity + k3*steer_angle)

# Runs one control cycle of the autonomous bicycle in a fixed interval defined 
# by PERIOD
# Reads IMU data, reads potentiometer data, calculates output to the motor,
# and sends motor output to the motor
# @param: start_time- the starting time of this instance of control_cycle
def control_cycle(start_time):
	imu_data = imu.get_roll_angle_ang_rate(imu_serial_port)
	
	# Check orientation of IMU
	lean_angle = imu_data[0]
	lean_velocity = imu_data[2] #AngRateY
	steer_angle = pot.get_angle()

	# Output to motor
	target_velocity = calculate(lean_angle, lean_velocity, steer_angle) 
	motor.control_motor(target_velocity, time.time())			
	
	# Calculate left over time to wait
	extra_time = PERIOD - (time.time() - start_time)
	time.sleep(extra_time)

while True:
	control_cycle(time.time())
