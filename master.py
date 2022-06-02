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

from os import extsep
import RPi.GPIO as IO
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.cleanup()
IO.setmode(IO.BCM)

run = True #set to false for exiting

#if your actuator needs more complicated conrolls than a high singnal on a single pin, write it into a functinon here
def fan(a):
    print("fan")
    IO.output(3,IO.LOW)
    sleep(3)
    IO.output(3,IO.HIGH)
    
def led(a):
    print("led")
    IO.output(5,IO.HIGH)
    sleep(2)
    IO.output(5,IO.LOW)
    
def servo():
    print("servo")
    pwm = GPIO.PWM(7,50)
    pwm.start(0)
    IO.output(7,True)
    pwm.ChangeDutyCycle(7)
    sleep(1)
    GPIO.output(7,False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    
def motor():
    print("motor")
    i = 0
    while i<100:
        sleep(.1)
        IO.output(21,IO.HIGH)
        sleep(.1)
        IO.output(21,IO.LOW)
        i += 1
    
    
class IOPair:   #class containg information on input / output pair
    pinIn = 0
    pinOut = 0
    func = 0
    initial = 0
    
    def __init__(self, inPin, outPin, ini, outFunc):
            pinIn = inPin   #pin number to activate, NOTE output will be executed on change HIGH to LOW and on LOW to HIGH
            pinOut = outPin
            func = outFunc
            initial = ini

   
#loop that waits for an interrupt and has an conditional exit
def loop():
    try:
        while True:
            sleep(.1)
    except KeyboardInterrupt:
        IO.Cleanup()
        inp = input("terminate program [Yes/NO] ?")
        if inp == "Yes" or inp=="Y"or inp=="y"or inp=="yes":
            Clean()
        else: loop()

#execute to exit program
def Clean():
    print("exiting")
    #preform cleanup on used pins when exiting
    for x in list:
        IO.cleanup(x.pinIn)
        IO.cleanup(x.pinOut)
    exit()

#list of input output pairs with examples
# to add an actuator sensor pair ass a new IOPair(input , output) to the list below
list = [IOPair(2,3,IO.HIGH,fan),IOPair(4,5,IO.LOW,led),IOPair(6,7,IO.LOW,servo),IOPair(6,9,IO.LOW,motor)]
 
#preform setup for all items in list
for x in list:        
    IO.setup(x.pinIn,IO.IN)
    IO.add_event_detect(x.pinIn, IO.BOTH, bouncetime=300)        # let us know when the pin goes HIGH or LOW
    
    IO.setup(x.pinOut, IO.OUT,initial = x.initial)
    IO.add_event_callback(x.pinIn, x.func)  # assign function to GPIO PIN, Run function on change 

#wait for input
loop()
