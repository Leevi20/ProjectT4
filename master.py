from doctest import OutputChecker
import RPi.GPIO as IO
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BCM)

def callback(): #example function
    print("happening!!!!")

class IOPair:   #class containg information on input / output pair
    pinIn = 0
    pinOut = 0
    
    def __init__(inPin, outPin):
        if (type(inPin)is int)and (type(outPin)is int or type(outPin)is function):
            pinIn = inPin   #pin number to activate, NOTE output will be executed on change HIGH to LOW and on LOW to HIGH
            pinOut=outPin   #NOTE can be an intiger for a output pin OR a function to be callled
        
        else:
            print("Error: invalid parameters in IO pair constructor")

list = [IOPair(7,8), IOPair(9,callback)]    #list of input output pairs with examples
    
#preform setup for all items in list
for x in list:        
    IO.setup(x.pinIn,IO.IN)
    IO.add_event_detect(x.pinIn, IO.BOTH, bouncetime=300)        # let us know when the pin goes HIGH or LOW
    
    #if pinOut is an intiger set the matching pin on GPIO to HIGH, NOTE is it possible to just connect thease wires?
    if type(x.pinOut) is int:   
        IO.setup(x.pinOut, IO.OUT)
        IO.add_event_callback(x.pinIn, IO.output(x.pinOut,IO.HIGH))  # assign function to GPIO PIN, Run function on change
    
    #if pinOut is a function call it, NOTE if pinOut isn't a in it's a function, see typeCheck in IOPair _init_
    else:
        IO.add_event_callback(x.pinIn, x.pinOut)  
        
#loop that waits for an interrupt and has an conditional exit
run = True
while run:
            
    try:
        i = input()
    except KeyboardInterrupt:
        print("want to exit? Y/N")
        i = input()
        if(i=="Y" or i == "Yes" or i =="yes"):
            run = False
    sleep(.1)

#preform cleanup on used pins when exiting
for x in list:
    IO.cleanup(x.pinIn)
    if type(x.pinOut)==int:
        IO.cleanup(x.pinOut)