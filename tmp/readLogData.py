from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

time , distance , FSRvalue , EndStop , TopClass = np.loadtxt('dataLog.csv' , unpack=True , delimiter=",")

fig , axs =  plt.subplots(4 , sharex=True )
fig.suptitle('Gripper Data Log')
axs[0].plot( time , distance)
axs[0].set( ylabel = 'Sonic [cm]' )
axs[1].plot( time , FSRvalue)
axs[1].set( ylabel = 'FSR [volts]')
axs[2].plot( time , EndStop)
axs[2].set( ylabel = 'End Stop [-]' )
axs[3].plot( time , TopClass)
axs[3].set( ylabel = 'Detection' )

plt.show()