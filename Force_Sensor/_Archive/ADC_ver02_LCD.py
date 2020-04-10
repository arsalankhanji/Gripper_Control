from time import sleep
import Adafruit_ADS1x15
from Adafruit_CharLCD import Adafruit_CharLCD

# initializing ADC
adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)

# initializing LCD
lcd = Adafruit_CharLCD(rs=25, en=24, d4=23, d5=18, d6=15, d7=14, cols=16, lines=2 )

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
    
    lcd.clear()
    lcd.message("{0:0.3f}V [{1}]\n".format(volts, value[0]))
    lcd.message(" Mladman Systems\n")
    sleep(1)
