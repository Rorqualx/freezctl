from ast import Break
import time
import Adafruit_DHT
import sys
import gpiozero
import os
import subprocess

# Triggered by the output pin going high: active_high=True.

#GPIO Pinout
PRIME_PUMP = 6
LOW_VENT = 5
HIGH_VENT = 4

#This tells us which GPIO Pin triggers a corresponding relay 
relay1 = gpiozero.OutputDevice(LOW_VENT, active_high=True, initial_value=False)
relay2 = gpiozero.OutputDevice(PRIME_PUMP, active_high=True, initial_value=False)
relay3 = gpiozero.OutputDevice(HIGH_VENT, active_high=True, initial_value=False)

# DHT11 is the module used to take temperature measurments
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

# Time to prime the pad in seconds
PRIMETIME=3
PRINTTIME=1
LOOPTIME=30

#This code creates variables with the sensor information from the DHT22 module connected on GPIO pin 17 and then converts the temperature reading into a float number
#The try block attempts to read the sensors and convert the celsius reading to Farenheit and print it on the console and returning the value. If the system is unable to read the sensor the except block will print out an error and restart the program. 
def startup():
    global Temp_in_F
    try:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        Temp_in_F = (float(temperature * 9/5.0 + 32))
        print("Current Temperature={0:0.1f}f Current Humidity={1:0.1f}%".format(temperature * 1.8 + 32, humidity))
        return Temp_in_F
    except TypeError:
        print("Failed to retrieve current temperature, trying agin")
        time.sleep(PRINTTIME)
        subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:]) 
    except NameError:
        print("Name error")

#This block of code updates the program with the latest DHT sensor reading
def refresh_temp():
    global Temp_in_F
    try:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        print("Current Temperature={0:0.1f}f Current Humidity={1:0.1f}%".format(temperature * 1.8 + 32, humidity))
        Temp_in_F = (float(temperature * 9/5.0 + 32))
    except TypeError:
        print("Failed to retrieve current temperature, trying agin")
        time.sleep(PRINTTIME)    
        
#This function asks the user to input their name        
def name():
    name = input("Hello Please Enter Your Name: ")
    print("Welcome " + name +"!")
    
#this function allows the user to enter a new temperature
def chg_temp():
    global Set_temp
    Set_temp = float (input ("Please enter your desired temperature between 50°F and 80°F "))
    print(Set_temp)
    time.sleep(PRINTTIME)

#this function asks the user if they want set a specific temperature or set to a default temperature       
def tempint():
    try:
        change_temp = input("Temperature will be set to 72 dgrees Farenheit if temperature is not changed. Do you wish to change the temperature? Use Y or N to choose.")
        if change_temp == "y":
            chg_temp()
        elif change_temp =="n":
            print("Temperature will reamin as default 72 degrees")
            def_temp()
    finally:
        time.sleep(PRINTTIME)

#this function sets the temperature to 72 degrees as the default temperature
def def_temp():
    global Set_temp
    Set_temp = float(72)
    print("default temperture set")

#this function evaluates if the swamp cooler needs to start the pump to draw water oveer the pads
def prime_Option():
    try:
        while (Temp_in_F , Set_temp):
            if Temp_in_F > Set_temp:
                time.sleep(PRINTTIME)
                prime_Pad()
                break
            elif Temp_in_F < Set_temp:
                print("Priming is not necessary")
                time.sleep(PRINTTIME)
                Idle_loop()
            else:
                print("something went wrong in the prime option function")
    except NameError:
            time.sleep(PRINTTIME)

#If the prime_Option function determines that priming the pads is neccessary this function will turn the pump on and strt a 5 min timer.            
def prime_Pad():
    try:
        print ("Priming Pads")
        relay2.on()
        seconds = 3
        while seconds > 1:
            mins, secs = divmod (seconds, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print (timer, end=" Minutes Remaining\r")
            seconds -= 1
            time.sleep(PRINTTIME)
        relay2.off()
        print ("Priming swampcooler Pads is done")
    except:
        print("prime pad error")

#this function checks if the temperature is still above the set temperature and calls the refresh function to update the sensor data before evaluating the condition again. Id the condition is true then High cool function is maintained when the condition is no loger true it triggers the Idle loop. 
def Main_loop():
    try:
        while (Temp_in_F , Set_temp):
            if Temp_in_F > Set_temp:
                print("Turning on cooling cycle")
                high_cool_loop()
            elif Temp_in_F < Set_temp:
                print ("Swamp cooler now switching to idle mode")
                Idle_loop()
            else:
                print("something went wrong in the Main loop")
                time.sleep(PRINTTIME)
    except NameError:
        print ("main loop error") 

def high_cool_loop():
    try:
        while (Temp_in_F , Set_temp):
            if Temp_in_F > Set_temp:
                high_Cool()     
                print("Cooling Cycle Running")
                refresh_temp()
                time.sleep(PRINTTIME) 
            elif Temp_in_F == Set_temp + 1:
                print("Low cooling on until desired temperture is met.")
                high_cool_off()
                low_cool_on()
                print("Low cool on")
                refresh_temp()
                time.sleep(PRINTTIME)
            elif Temp_in_F < Set_temp:
                print("Cooling cycle done")
                high_cool_off()
                time.sleep(PRINTTIME)
                Idle_loop()
            else:
                print("Something went wrong durring the cooling cycle")
    except:
        print("Cooling cycle error")
           
#this function refreshes the temperature and checks if the main loop needs to be triggered             
def Idle_loop():
    try:
        while (Temp_in_F , Set_temp):
            if Temp_in_F <= Set_temp:
                print("Thermostat is now in Idle mode")
                time.sleep(PRINTTIME)
                refresh_temp()
                time.sleep(PRINTTIME)              
            elif Temp_in_F == Set_temp + 1:
                print("Waking from idle loop")
                refresh_temp()
                time.sleep(PRINTTIME)
                break
            else:
                print("something went wrong in the Idle loop")
                time.sleep(PRINTTIME)
                refresh_temp()
                break
    except:
        print("idle loop error")
                  
#this function turns on the high fan and pump             
def high_Cool():
        print ("High Cool On")
        relay3.on()
        relay2.on()
#this function turns off the high fan and pump
def high_cool_off():
        relay3.off()
        relay2.off()

def low_cool_on():
        relay1.on()
        relay2.on()
        
def low_cool_off():
        relay1.off()
        relay2.off()        

def pump_on():
        relay2.on()
        
def pump_off():
        relay2.off()
        
# program logic starts here
if __name__ == "__main__":
    try:
        startup()
        name()
        tempint()
        prime_Option()
        Main_loop()
    except KeyboardInterrupt:
        print("\nExiting application\n")
        # exit the application
        sys.exit(0)
