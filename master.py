from asyncio import wait_for
from doctest import OutputChecker
import rpi.GPIO as IO
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BCM)

def callback(): 
    print("happening!!!!")

class IOPair:
    pinIn = 0
    pinOut = 0
    
    def __init__(input, output):
        if type(input)is int:
            pinIn = input
            pinOut=output
        
        else:
            print("Error: invalid parameters in IO pair constructor")
        
    def Sethigh():
        IO.output(pinOut,IO.HIGH)

list = [IOPair(7,8), IOPair(9,callback)]
    
for x in list:
    IO.setup(x.pinIn,IO.IN)
    
    if type(x.pinOut) is int:   #if pinOut is an intiger set the matching pin on GPIO to HIGH
        IO.setup(x.pinOut, IO.OUT)
        IO.add_event_detect(x.pinIn, IO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
        IO.add_event_callback(x.pinIn, x.SetHigh())  # assign function to GPIO PIN, Run function on change
    
    else:                       #if pinOut is a function call it
        IO.add_event_detect(x.pinIn, IO.BOTH, bouncetime=300) 
        IO.add_event_callback(x.pinIn, x.pinOut)  
        

run = True
while run:
    try:
        i = input()
    except KeyboardInterrupt:
        print("want to exit? Y/N")
        i = input()
        if(i=="Y" or i == "Yes" or i =="yes"):
            run = False
    sleep(1)