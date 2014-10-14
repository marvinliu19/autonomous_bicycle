# Main control for the robotic bicycle
import Adafruit_BBIO.UART as UART
import serial
import time
import imu 
import potentiometer

# Constants
PERIOD = 0.1 		# Seconds per calculation cycle
POT_PIN = 'P9_40'	# Input pin on BeagleBone Black for potentiometer

# Initialize serial port for the IMU
UART.setup("UART4")
imu_serial_port = serial.Serial(port = "/dev/ttyO4", baudrate=115200, 
	parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, 
	bytesize=serial.EIGHTBITS, timeout=0, xonxoff=0, rtscts=0)

###############################################################################

# Calculates voltage given lean angle and steer angle
# Precondition: Lean is the range -pi-pi and steer is in the range 0-360
# Postcondition: Return voltage in range 0-3.3V
def motor_output(lean, steer):
	return 0

def control_cycle(start_time):
	lean_angle = imu.get_roll_angle(imu_serial_port)
	steer_angle = read_steer_angle()
	
	# Output to motor
	motor_output(roll_angle, steer_angle)			
	
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

	
	


