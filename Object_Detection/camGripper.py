######################################################
#                CAMERA FEED SCRIPT                  #
######################################################
# Version: 1.00                                      #                    
# Date: 18 April 2020                                #
# Author: Arsalan                                    #
#----------------------------------------------------#
## Some of the code is copied from:                 ##
## https://github.com/EdjeElectronics/              ##
######################################################

# Import packages
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime

# Set up camera constants
IM_WIDTH = 640 # 1280   #  Use smaller resolution for
IM_HEIGHT = 480 # 720   #  faster framerate
camera_type = 'picamera'
frameRate = 24 # fps

def startCamera(frame_rate_calc, stopFlag , lock):

    currentDT = datetime.datetime.now()
    currentDT = currentDT.strftime("%Y-%m-%d_%H-%M-%S")
    FILE_OUTPUT = '/home/pi/Gripper_Control/Object_Detection/videos/cameraOutput_%s.mp4' %(currentDT)
    
    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter(FILE_OUTPUT,cv2.VideoWriter_fourcc('m','p','4','v'), frameRate, (IM_WIDTH,IM_HEIGHT))

    # Initialize frame rate calculation
    #frame_rate_calc = 1
    freq = cv2.getTickFrequency()
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Initialize Picamera and grab reference to the raw capture
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = frameRate
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        t1 = cv2.getTickCount()
        
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        frame = np.copy(frame1.array)
        frame.setflags(write=1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_expanded = np.expand_dims(frame_rgb, axis=0)

        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc.value),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Gripper Camera', frame)
        
        # Write final frame
        out.write(frame)
        
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc.value = 1/time1
        
        # Press 'q' to quit
        if (cv2.waitKey(1) == ord('q')) or (stopFlag.value==1):
            break

        rawCapture.truncate(0)

    camera.close()
    out.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':  # Program entrance
    startCamera(1,0,0)

