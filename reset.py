######################################################
#              RESET GRIPPER SCRIPT                  #
######################################################
# Version: 1.00                                      #                    
# Date: 04 May 2020                                  #
# Author: Arsalan                                    #
#----------------------------------------------------#
#----------------------------------------------------#
######################################################

# Importing Modules
from Motor_Control import motorControl as mc
from Push_Button import pushButton as pb
import time

# Initializing Modules
mc.setup() # initializing Motor Control
pb.setup() # initializing Push Button / End Stop Switch

# setting variables
dutyCycle = 40 # varies from 0-100%
    
#--------------------#    
#   MAIN PROGRAM     #
#--------------------#
try:
    print('Resetting Gripper ...')
    print('********************************************')
    print("**  Press 'Ctrl + C' to terminate script  **")
    print('********************************************')
    while(True):
        
        status = pb.getButton()
        
        if status==1:
            mc.motorStop()
            mc.destroy()
            print('Gripper Reset!')
            break
        elif status == 0:
            mc.motor(dutyCycle) # open gripper     
                       
except KeyboardInterrupt: # Press ctrl-c to end the program.
    mc.motorStop()
    mc.destroy()

        
        
        
        

