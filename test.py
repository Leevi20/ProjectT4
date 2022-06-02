import RPi.GPIO as IO
from time import sleep

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.cleanup()
IO.setmode(IO.BCM)

IO.setup(4,IO.IN)
IO.setup(5,IO.OUT,initial=IO.LOW)