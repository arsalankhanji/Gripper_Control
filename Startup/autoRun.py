#!/usr/bin/python
from time import sleep
import logging
import datetime
 
currentDT = datetime.datetime.now()
currentDT = currentDT.strftime("%Y-%m-%d_%H-%M-%S")

logFilePath = '/home/pi/Gripper_Control/tmp/status_%s.log' %(currentDT)
logging.basicConfig(filename=logFilePath,level=logging.DEBUG)
logging.info('Date: %s' %(str(currentDT)))
logging.debug('Debuggin messages go here')
logging.info('This is a test script')
logging.warning('warning messages go here')

for x in range(100):
    sleep(1)
    logging.info(x)