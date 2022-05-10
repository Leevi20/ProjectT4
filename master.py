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
    
    def __init__(input, output):
        if type(input)is int:
            pinIn = input   #pin number to activate NOTE output will be executed on change HIGH to LOW and on LOW to HIGH
            pinOut=output   #NOTE can be an intiger for a output pin OR a function to be callled
        
        else:
            print("Error: invalid parameters in IO pair constructor")

list = [IOPair(7,8), IOPair(9,callback)]    #list of input output pairs with examples
    
#preform setup for all items in list
for x in list:        
    IO.setup(x.pinIn,IO.IN)
    
    #if pinOut is an intiger set the matching pin on GPIO to HIGH
    if type(x.pinOut) is int:   
        IO.setup(x.pinOut, IO.OUT)
        IO.add_event_detect(x.pinIn, IO.BOTH, bouncetime=300)        # let us know when the pin goes HIGH or LOW
        IO.add_event_callback(x.pinIn, IO.output(x.pinOut,IO.HIGH))  # assign function to GPIO PIN, Run function on change
    
    #if pinOut is a function call it
    else:                       
        IO.add_event_detect(x.pinIn, IO.BOTH, bouncetime=300) 
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