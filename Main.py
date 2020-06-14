######################################################
#             MASTER CONTROL SCRIPT                  #
######################################################
# Version: 1.03                                      #                    
# Date: 04 May 2020                                #
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
# DONOT stop script by terminating script as the     #
# motor might go in overspeed with full duty cycle   #
# INSTEAD USE "Ctrl + C"                             #
#----------------------------------------------------#
######################################################

# Importing Modules
from Motor_Control import motorControl as mc
from Ultrasonic_Sensor import ultrasonicRanging as ur
from Force_Sensor import ADC as adc
from Push_Button import pushButton as pb
from Object_Detection import camGripper, camTensorFlow
import multiprocessing
from multiprocessing import Value, Array, Lock
import time
import csv

# INPUTS
camSelect = 0  # || 0 -> Simple Camera || 1-> TensorFlow Detector || 2 -> TensorFlow LITE Detector
alpha = 0.5    # Exponential Moving Average (EMA) Filter Alpha. Alpha = 1 --> no filtering

# Initializing Modules
mc.setup() # initializing Motor Control
ur.setup() # initializing Ultrasonic Sensor
pb.setup() # initializing Push Button / End Stop Switch

# Initializing Data Logger
logFile = open("tmp/dataLog.csv" , "w" , newline="")
csvObj = csv.writer(logFile)

# Initializing Clock
absStartTime = time.time()

# setting variables
dutyCycle = 80 # varies from 0-100%
minGripDist = 2.0 # cm. [min. gripping distance]
maxGripDist = 12.0 # cm. [max. gripping distance]
ADCthresh = 3.0 # volts. [ADC value threshold for tight grip]

# creating shared variables for multi-processing
frameRate = Value('f',1)
stopFlag = Value('i',0)
lock = Lock()

# selecting camera detection type
if camSelect == 0 :
    # Start Camera Feed (parallel process 1)
    print('Initializing Camera ...')
    P1 = multiprocessing.Process(target=camGripper.startCamera , args=(frameRate,stopFlag,lock) )
    P1.start()
elif camSelect == 1 :
    # Start TF Object Detection (parallel process 1)
    print('Initializing Camera & Detection ...')
    classes = Array('f',5) # creating shared variable to access detected classes
    scores = Array('f',5) # creating shared variable to access detected class scores
    P1 = multiprocessing.Process(target=camTensorFlow.startObjectDetect , args=(frameRate,classes, scores, stopFlag,lock) )
    P1.start()
elif camSelect == 2 :        
    # Start TF Lite Object Detection (parallel process 1)
    print('Initializing Camera & Detection ...')
    print('WARNING! Functionality Under Development ...')

#--------------------------------------------------------#       
#--------------------------------------------------------#    
#                     MAIN PROGRAM                       #
#--------------------------------------------------------#
#--------------------------------------------------------#
try:
    print('Initializing Gripper Control ...')
    print('********************************************')
    print("**  Press 'Ctrl + C' to terminate script  **")
    print('********************************************')
    loopCount = 1
    distance_old = ur.getSonar()
    
    while(True):
        distanceRaw = ur.getSonar()
        ADCvalue = adc.getADC()
        status = pb.getButton()
        # Filtering Sonic Distance with EMA Filter
        distance = (1 - alpha)*distance_old + alpha*distanceRaw
        distance_old = distance
        # ------------- USE For Debugging Only -------------#
        #print(classes[:]) 
        #print(scores[:])
        #print ("%.2f cm , %.2f volts , %i "%(distance,ADCvalue,status))
        # --------------------------------------------------#
        
        if camSelect == 0:
            topClass = 75
        elif camSelect == 1:
            topClass = classes[0]  # 75 is remote and 77 is cell phone in label map
        elif camSelect == 2:
            topClass = classes[0]
        
        if (topClass == 77) or (topClass == 75):
            if ((minGripDist<distance<maxGripDist) & (ADCvalue>ADCthresh)):
                mc.motor(-dutyCycle) # close gripper          
            elif ((minGripDist<distance<maxGripDist) & (ADCvalue<ADCthresh)):
                mc.motorStop()
            elif ( (distance>maxGripDist) & (ADCvalue>ADCthresh)):
                if status==1:
                    mc.motorStop()
                elif status == 0:
                    mc.motor(dutyCycle) # open gripper 

        currentTime = time.time() - absStartTime
        csvObj.writerow([ round(currentTime,2) , round(distanceRaw,2) , round(ADCvalue,2) , round(status,0) , round(topClass,2) , round(distance,2) ])
        
        loopCount = loopCount + 1        
                 
                       
except KeyboardInterrupt: # Press ctrl-c to end the program.
    mc.motorStop()
    mc.destroy()
    with lock:
        stopFlag.value = 1
    #P1.terminate() # for force closing the process
        
        
        
        
