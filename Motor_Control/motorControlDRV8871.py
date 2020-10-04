######################################################
#        DC Motor Control Script for DRV8871         #
######################################################
# Version: 1.00                                      #                    
#----------------------------------------------------#
######################################################

import RPi.GPIO as GPIO
import time

# define the pins connected to DRV8871 
motoRPin1 = 27 
motoRPin2 = 17 

def setup():
    global p1 p2
    #GPIO.setwarnings(False) # Turning off warnings
    GPIO.setmode(GPIO.BCM) # Broadcom Memory mode  
    GPIO.setup(motoRPin1,GPIO.OUT)   # set pins to OUTPUT mode
    GPIO.setup(motoRPin2,GPIO.OUT)
        
    #p1 = GPIO.PWM(motoRPin1,1000) # creat PWM and set Frequence to 1KHz
    #p2 = GPIO.PWM(motoRPin2,1000) # creat PWM and set Frequence to 1KHz
    #p1.start(0)
    #p2.start(0)
    
# motor function: determine the direction and speed of the motor according to the input values 
def motor(value):
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
    #p.start(abs(value))
    #print ('The PWM duty cycle is %d%%\n'%(abs(value)))   # print PMW duty cycle.
    
def motorStop():
    #p.start(0)
    #p.stop()
    print ('Motor Stop...')

def destroy():
    GPIO.cleanup()
    
if __name__ == '__main__':  # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        value = -40 # ?? closes / ?? opens
        motor(value)
    except KeyboardInterrupt: # Press ctrl-c to end the program.
        destroy()
