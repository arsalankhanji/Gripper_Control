######################################################
#             MASTER CONTROL SCRIPT                  #
######################################################
# Version: 1.01                                      #                    
# Date: 10 April 2020                                #
# Author: Arsalan                                    #
# **********PLEASE NOTE******************************#
# This script is gonna go obsolete soon as we are    #
# moving to using a DC motor as Gripper Engine       #
#----------------------------------------------------#
#-------------Stepper Control Help-------------------#
# numRev = 1; # number of revolutions the stepper has to make
# tRev = 0.2; # lower tRev means fast speed low torque and vice versa
# dirRev = 0; # 1 is CW and 0 is CCW
# sc.moveGripper(numRev,tRev,dirRev)
#----------------------------------------------------#
#----------------Sonic Sensor Help-------------------#
# distance = ur.getSonar() # where distance is in cm
#----------------------------------------------------#
#----------------------------------------------------#
#--------------------ADC Help------------------------#
# ADCvalue = adc.getADC() # where value is in volts
#----------------------------------------------------#
######################################################

from Stepper_Control import stepperControl as sc
from Ultrasonic_Sensor import ultrasonicRanging as ur
from Force_Sensor import ADC as adc
from Push_Button import pushButton as pb
import time

sc.setup() # initializing Stepper Control
ur.setup() # initializing Ultrasonic Sensor
pb.setup() # initializing Push Button

while(True):
    distance = ur.getSonar()
    ADCvalue = adc.getADC()
    status = pb.getButton()
    
    if ((4.0<distance<9.0) & (ADCvalue<1.65)):
        sc.moveGripper(1,0.2,1)
        
        
        