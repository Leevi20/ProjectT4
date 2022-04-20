import RPi.GPIO as IO
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BCM)

inputPins = [7]

for x in inputPins:
    IO.setup(x,IO.IN)
    