import Adafruit_BBIO.PWM as PWM

duty_cycle_pin = "P8_13"
direction_pin = "P8_19"

PWM.stop(duty_cycle_pin)
PWM.stop(direction_pin)

PWM.cleanup()
