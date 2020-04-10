from time import sleep
import RPi.GPIO as GPIO

DIR = 20 # Direction GPIO pin
STEP = 21 # Step GPIO pin
CW = 1 # Clockwise rotation
CCW = 0 # Counterclockwise rotation
SPR = 400 # Steps per revolution (360/0.9)

GPIO.setmode(GPIO.BCM) # Broadcom Memory mode
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, CCW)

step_count = 5*SPR # number of revolutions
delay = 0.1/SPR # speed of motor in seconds per revolution

for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
    
sleep(0.5)
GPIO.output(DIR, CW)
for x in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
    
    
