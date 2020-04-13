# Setting up Python Script Auto-run            

Reference Tutorial: https://www.youtube.com/watch?v=zRXauWUumSI

# Auto-run Script Setup
In a terminal window type :

$ sudo crontab -e

Scroll to the bottom and add the following line :

@reboot python /home/pi/Gripper_Control/Startup/autoRun.py &

Type “Ctrl+X” to exit, then press “Y” to save and then press “Enter”.