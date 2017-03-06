#! /usr/bin/env python3

import os
from time import sleep
import signal
import sys
import RPi.GPIO as IO

IO.setwarnings(False)

IO.setmode(IO.BCM)
IO.setup(19, IO.OUT)
s = IO.PWM(19, 100)

IO.setup(18, IO.OUT)
t = IO.PWM(18, 100)

if (sys.argv[1] == 't'):
    duty = sys.argv[2]
    t.start(float(duty))

if (sys.argv[1] == 's'):
    duty = sys.argv[2]
    s.start(float(duty))
