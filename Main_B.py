######################################################
#             MASTER CONTROL SCRIPT                  #
######################################################
# Version: 1.01                                      #                    
# Date: 17 April 2020                                #
# Author: Arsalan                                    #
#----------------------------------------------------#
#---------------Motor Control Help-------------------#
# NOTE: As motor runs at high speed make sure the    #
# motor wires are not too close to the ADC inputs    #
# otherwise it will destroy input from Force Sensor  #
# mc.motor(dutyCycleValue) # -100 to 100. - signs reversers direction
# mc.motorStop()
#----------------------------------------------------#
#----------------Sonic Sensor Help-------------------#
# distance = ur.getSonar() # where distance is in cm
#----------------------------------------------------#
#----------------------------------------------------#
#--------------------ADC Help------------------------#
# ADCvalue = adc.getADC() # where ADC value is in volts
#----------------------------------------------------#
#----------------------------------------------------#
#----------------------WARNING-----------------------#
# DONOT stop script by pressing red button as the    #
# motor might go in overspeed with full duty cycle   #
# INSTEAD USE "Ctrl + C"                             #
#----------------------------------------------------#
######################################################

from Motor_Control import motorControl as mc
from Ultrasonic_Sensor import ultrasonicRanging as ur
from Force_Sensor import ADC as adc
from Push_Button import pushButton as pb
from Object_Detection import camGripper
import multiprocessing
import time

mc.setup() # initializing Motor Control
ur.setup() # initializing Ultrasonic Sensor
pb.setup() # initializing Push Button

# setting variables
dutyCycle = 80 # varies from 0-100%
minGripDist = 2.0 # cm. [min. gripping distance]
maxGripDist = 10.0 # cm. [max. gripping distance]
ADCthresh = 2.6 # volts. [ADC value threshold for tight grip]

# Start Camera Feed (parallel process 1)
P1 = multiprocessing.Process(target=camGripper.startCamera)
P1.start()

try:        
    while(True):
        distance = ur.getSonar()
        ADCvalue = adc.getADC()
        status = pb.getButton()
        
        if ((minGripDist<distance<maxGripDist) & (ADCvalue<ADCthresh)):
            mc.motor(-dutyCycle) # close gripper          
        elif ((minGripDist<distance<maxGripDist) & (ADCvalue>ADCthresh)):
            mc.motorStop()
        else:
            if status==1:
                mc.motorStop()
            else:
                mc.motor(dutyCycle) # open gripper      
            
except KeyboardInterrupt: # Press ctrl-c to end the program.
    mc.motorStop()
    mc.destroy()
    P1.terminate()
        
        
        
        
