######################################################
#             Ultrasonic Ranging Script              #
######################################################
# Version: 1.00                                      #                    
#----------------------------------------------------#
######################################################

import RPi.GPIO as GPIO
#import numpy as np # Debugging Only
import time

trigPin = 23
echoPin = 24
MAX_DISTANCE = 220          # define the maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE*60   # calculate timeout according to the maximum measuring distance

def pulseIn(pin,level,timeOut): # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
    
def getSonar():     # get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      # make trigPin output 10us HIGH level 
    time.sleep(0.00001)     # 10us
    GPIO.output(trigPin,GPIO.LOW) # make trigPin output LOW level 
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   # read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # calculate distance with sound speed 340m/s 
    return distance
    
def setup():
    GPIO.setwarnings(False) # Turning off warnings
    GPIO.setmode(GPIO.BCM)      # use Broadcom Memory mode
    GPIO.setup(trigPin, GPIO.OUT)   # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)    # set echoPin to INPUT mode

def loop():
#    distance_vec = np.array([])     # Debugging Only
    while(True):
        distance = getSonar() # get distance
        print ("The distance is : %.2f cm"%(distance))
        #time.sleep(1)
        ## for Debuggins ##
#        distance_vec = np.append(distance_vec,distance) # Debugging Only
#        print(distance_vec) # Debugging Only
        
if __name__ == '__main__':     # Program entrance
    print ('Sonic Sensor is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        GPIO.cleanup()         # release GPIO resource


    

