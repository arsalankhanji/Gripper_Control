######################################################
#             MASTER CONTROL SCRIPT                  #
######################################################
# Version: 1.00                                      #                    
# Date: 13 April 2020                                #
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
# distance = ur.getSonar() # where distance is in cm
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
import time

mc.setup() # initializing Motor Control
ur.setup() # initializing Ultrasonic Sensor
pb.setup() # initializing Push Button

try:        
    while(True):
        distance = ur.getSonar()
        ADCvalue = adc.getADC()
    #    status = pb.getButton()
    #    if ((distance<9.0) & (status==0)):
        if ((4.0<distance<10.0) & (ADCvalue<1.65)):
            mc.motor(30)
        else:
            mc.motorStop()
            
except KeyboardInterrupt: # Press ctrl-c to end the program.
    mc.motorStop()
    mc.destroy()
        
        
        
        
