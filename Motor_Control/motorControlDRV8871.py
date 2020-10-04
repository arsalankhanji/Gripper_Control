######################################################
#        DC Motor Control Script for DRV8871         #
######################################################
# Version: 1.00                                      #                    
#----------------------------------------------------#
######################################################

import RPi.GPIO as GPIO
import time

# define the pins connected to L293D 
motoRPin1 = 27 
motoRPin2 = 17 
enablePin = 22
standbyPin = 5

def setup():
    global p
    #GPIO.setwarnings(False) # Turning off warnings
    GPIO.setmode(GPIO.BCM) # Broadcom Memory mode  
    GPIO.setup(motoRPin1,GPIO.OUT)   # set pins to OUTPUT mode
    GPIO.setup(motoRPin2,GPIO.OUT)
    GPIO.setup(enablePin,GPIO.OUT)
    GPIO.setup(standbyPin,GPIO.OUT)
        
    p = GPIO.PWM(enablePin,1000) # creat PWM and set Frequence to 1KHz
    p.start(0)
    
# motor function: determine the direction and speed of the motor according to the input ADC value input
def motor(value):
    GPIO.output(standbyPin,GPIO.HIGH)
    if (value > 0):  # make motor turn forward
        GPIO.output(motoRPin1,GPIO.HIGH)  # motoRPin1 output HIHG level
        GPIO.output(motoRPin2,GPIO.LOW)   # motoRPin2 output LOW level
        #print ('Turn Forward...')
    elif (value < 0): # make motor turn backward
        GPIO.output(motoRPin1,GPIO.LOW)
        GPIO.output(motoRPin2,GPIO.HIGH)
        #print ('Turn Backward...')
    else :
        GPIO.output(motoRPin1,GPIO.LOW)
        GPIO.output(motoRPin2,GPIO.LOW)
        #print ('Motor Stop...')
    p.start(abs(value))
    #print ('The PWM duty cycle is %d%%\n'%(abs(value)))   # print PMW duty cycle.
    
def motorStop():
    p.start(0)
    p.stop()

def loop(value):
    print ('Duty Cycle is : %d %%'%(value))
    while True:
        motor(value)
        time.sleep(0.01) # 0.01

def destroy():
    GPIO.cleanup()
    
if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        value = -40 # -40 closes / +40 opens
        loop(value)
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
