#pins       old -> new
#flame      2 -> 4
#fan        3 -> 11 low to actuate
#prox       4 -> 3
#light      5 -> 2
#light sens 6 -> 14
#servo      7 -> 22
#humidity   8 -> 23
#DC motor INC    21
#DC motor I/U    20
#empty          5 & 10

import RPi.GPIO as IO
import dht11
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.cleanup()

run = True #set to false for exiting

#if your actuator needs more complicated conrolls than a high singnal on a single pin, write it into a functinon here
def fan(a):
    print("fan")
    IO.output(11,IO.LOW)
    sleep(3)
    IO.output(11,IO.HIGH)
    
def led(a):
    print("led")
    IO.output(2,IO.HIGH)
    sleep(2)
    IO.output(2,IO.LOW)
    
#servo actuattion code from Thabit
def servo(a):
    print("servo")
    pwm = GPIO.PWM(22,50)
    pwm.start(0)
    pwm.ChangeDutyCycle(7.5)
    sleep(.1)
    pwm.ChangeDutyCycle(72.5)
    sleep(.1)
    pwm.ChangeDutyCycle(12.5)
    sleep(.2)
    pwm.stop()
    
def motor(a):
    print("motor")
    i = 0
    while i<100:
        sleep(.1)
        IO.output(21,IO.HIGH)
        sleep(.1)
        IO.output(21,IO.LOW)
        i += 1
        
#empty function     
def empty(a):
    print("nothing")
    
class IOPair:   #class containg information on input / output pair
    pinIn = 0
    pinOut = 0
    func = empty
    initial = IO.LOW
    
    def PrintValues(self):
        print("pin in = " + str(self.pinIn))
        print("pin out = " + str(self.pinOut))
        print("function = " + str(self.func))
        print("initial out pin state = " + str(self.initial))
        print("")
    
    def __init__(self, inPin, outPin, ini, outFunc):
            self.pinIn = inPin   #pin number to activate, NOTE output will be executed on change HIGH to LOW and on LOW to HIGH
            self.pinOut = outPin
            self.func = outFunc
            self.initial = ini
            self.PrintValues()


#list of input output pairs with examples
# to add an actuator sensor pair ass a new IOPair(input , output) to the list below
list = [IOPair(4,11,IO.HIGH,fan),IOPair(3,2,IO.LOW,led),IOPair(14,22,IO.LOW,servo),IOPair(5,20,IO.LOW,motor),IOPair(10,21,IO.LOW,empty)]
 
#preform setup for all items in list
for x in list:
    print("setting up:")
    
    IO.setup(x.pinIn,IO.IN)
    IO.add_event_detect(x.pinIn, IO.BOTH,callback = x.func, bouncetime=300)        # let us know when the pin goes HIGH or LOW
    
    IO.setup(x.pinOut, IO.OUT,initial = x.initial)
    #IO.add_event_callback(x.pinIn, x.func)  # assign function to GPIO PIN, Run function on change 

#wait for input
print("press ctrl + c to exit")
try:
    while True:
        sleep(.1)
        result = dht11.DHT11(pin = 23).read()
        if result.is_valid():
            if result.humidity > .5: 
                motor()
        
except KeyboardInterrupt:
    print("exiting")
    IO.Cleanup()