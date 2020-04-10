import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(20,GPIO.OUT)
print("LED on")
GPIO.output(20,GPIO.HIGH)
time.sleep(10)
print("LED off")
GPIO.output(20,GPIO.LOW)