from time import sleep
import RPi.GPIO as GPIO

DIR = 20 # Direction GPIO pin
STEP = 21 # Step GPIO pin
SPR = 400 # Steps per revolution (360/0.9)

def setup():
    GPIO.setwarnings(False) # Turning off warnings
    GPIO.setmode(GPIO.BCM) # Broadcom Memory mode
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)

def moveGripper(numRev,tRev, dirRev):
    step_count = numRev*SPR # numRev is number of revolutions
    delay = tRev/SPR # tRev is speed of motor in seconds per revolution
    GPIO.output(DIR, dirRev) # dirRev is revolution direction. 1 for CW and 0 for CCW

    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    
    
    


