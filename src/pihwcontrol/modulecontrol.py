#! /usr/bin/env python3

from datacollect import read_temp

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
    target = sys.argv[2]
    while (read_temp() != target) {
        if (abs(read_temp() - target) > 40) {
            t.start(100)
        } else {
            t.start(50)
        }
    }
    t.start(0)

if (sys.argv[1] == 's'):
    duty = sys.argv[2]
    s.start(float(duty))
