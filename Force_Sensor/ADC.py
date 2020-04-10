from time import sleep
import Adafruit_ADS1x15

adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# Gain = 2/3 for reading voltages from 0 to 6.144V.
# See table 3 in ADS1115 Datasheet
GAIN = 2/3

# Main Loop
while 1:
    value = [0]
    # Read ADC channel 0
    value[0] = adc.read_adc(0, gain=GAIN)
    # Ratio of 16 bit value to max volts determines volts
    volts = value[0]/32767.0*6.144
    
    print(volts, value[0])