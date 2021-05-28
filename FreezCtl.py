#!/usr/bin/env python
# I am new to coding and this is my first program!  
import time
import Adafruit_DHT
import sys
import gpiozero

# Triggered by the output pin going high: active_high=True.

#GPIO Pinout
PRIME_PUMP = 7
LOW_VENT = 5
HIGH_VENT = 3

#This tells us which GPIO Pin will trigger the which relay 
relay2 = gpiozero.OutputDevice(PRIME_PUMP, active_high=True, initial_value=False)
relay1 = gpiozero.OutputDevice(LOW_VENT, active_high=True, initial_value=False)
relay3 = gpiozero.OutputDevice(HIGH_VENT, active_high=True, initial_value=False)

# DHT11 is the module used to take temperature measurments
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 17

# Time to prime the pad in seconds
PRIMETIME=5

PRIMED=0

name = input("Enter your name:")
print("Hello " + name + "!")

tempset = input ("What temperature would you like to set?")
result = int
print("Temperature set to" + tempset +"F" )

def gettemp():
    while True:
        temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if temperature is not None:
       print("Temp={0:0.1f}c".format(temperature))
    else:
        print("Sensor failure. Call Joe to Fix.");
    time.sleep(5);

def set_Relay():
        print("Powering: ON")

def prime_Pad():
        print ("Priming Pads")
        relay2.on()
        time.sleep(PRIMETIME)
        print ("Priming Pad's done")
        relay2.off()

def high_Cool ():
        print ("High Cool On")
        relay3.on()
        relay2.on()
        time.sleep(PRIMETIME)
        relay3.off()
        relay2.off()

def low_Cool ():
        print ("Low Cool On")
        relay1.on()
        relay2.on()
        time.sleep(PRIMETIME)
        relay1.off()
        relay2.off()

def low_Vent ():
        print("Fan on low")
        relay1.on()
        time.sleep(PRIMETIME)
        relay1.off()

def high_Vent ():
        print ("Fan on High")
        relay3.on()
        time.sleep(PRIMETIME)
        relay3.off()

# program logic starts here
if __name__ == "__main__":
    try:
        set_Relay()
        name
        tempset
        prime_Pad()
        high_Cool()
        low_Cool()
        high_Vent()
        low_Vent()
    except KeyboardInterrupt:
        print("\nExiting application\n")
        # exit the application
        sys.exit(0)
