######################################################
#                Push Button Script                  #
######################################################
# Version: 1.00                                      #                    
#----------------------------------------------------#
######################################################

import RPi.GPIO as GPIO

buttonPin = 18    # define buttonPin

def setup():
    GPIO.setwarnings(False) # Turning off warnings    
    GPIO.setmode(GPIO.BCM) # Broadcom Memory mode
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # set buttonPin to PULL UP INPUT mode

def loop():
    while True:
        if GPIO.input(buttonPin)==GPIO.LOW: # if button is pressed
            print ('Button Pressed >>>')     # print information on terminal
        else : # if button is relessed
            print ('Button Released <<<')    

def getButton():
    if GPIO.input(buttonPin)==GPIO.LOW: # if button is pressed
            status = 1    
    else : # if button is relessed
            status = 0
    return status

def destroy():
    GPIO.cleanup()                    # Release GPIO resource

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()

