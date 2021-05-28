#!/usr/bin/env python
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
DHT_SENSOR = Adafruit_DHT.DHT22
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
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                print("Temp={0:0.1f}c Humidity={1:0.1f}%".format(temperature, humidity))
            else:
                print("Sensor failure. Call Joe to Fix."); 
            time.sleep(2);

def set_Relay():
        print("Powering: ON")

def prime_Pad():
        print ("Priming Pads")
        relay2.on()
        time.sleep(PRIMETIME)
        print ("Priming Pad's done")
        relay2.off()

def prime_pad_Off():
        relay2.off()

def high_Cool():
        print ("High Cool On")
        relay3.on()
        relay2.on()

def high_cool_off():
        relay3.off()
        relay2.off()

def low_Cool():
        print ("Low Cool On")
        relay1.on()
        relay2.on()

def low_cool_Off():
        relay1.off()
        relay2.off()

def low_Vent():
        print("Fan on low")
        relay1.on()

def high_Vent():
        print ("Fan on High")
        relay3.on()

def high_vent_Off():
        relay3.off()

def is_tempMet(actualTemp,tempset):
     if (temperature <= tempset)
        return True 
     else: 
          False

def tempMetMinusOne():
     if (temperature = (tempset + 1))
         return True
     else:
          False

def tempMetMinusTwo():
     if (temperature = ((tempset + 2))
        return True 
     else:
          False

def Main_loop():
       is_tempMet = True
       if is_tempMet:
           print("Desired Temperature met")
           Print("Turining on fan on low")
           high_cool_Off
           low_Vent()
       elif tempMetMinusTwo = True
           high_vent_Off()
           low_Cool()
       elif tempMetMinusOne = True
           prime_pump_Off()
           low_Vent() 
       else
            print("Cooling Cycle Runing")
            prime_Pad()
            high_Cool()

# program logic starts here
if __name__ == "__main__":
    try:
        set_Relay()
        name
        tempset
        Main_loop()
    except KeyboardInterrupt:
        print("\nExiting application\n")
        # exit the application
        sys.exit(0)
