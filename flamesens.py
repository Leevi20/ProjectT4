import RPi.GPIO as IO

IO.setwarnings(False)
IO.setmode(IO.BCM)

inputPins = [7]

for x in inputPins:
    IO.setup(x,IO.IN)

def callback(): #add the things to do, once flame is detected here
    print("flame detected")
    
IO.add_event_detect(inputPins[0], IO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
IO.add_event_callback(inputPins[0], callback)  # assign function to GPIO PIN, Run function on change
 
# infinite loop
while True:
    time.sleep(1)