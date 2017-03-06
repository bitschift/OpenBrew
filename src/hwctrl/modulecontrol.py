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

def set_temp(temp):
    target = temp
    while (read_temp() != target) {
        if ((target - read_temp()) > 40) {
            t.start(100)
        } else if (target - read_temp() < 0) {
            t.start(0)  
        } else {
            t.start(50)
        }
    }
    t.start(0)

def set_stir(speed):
    duty = speed
    s.start(float(duty))
