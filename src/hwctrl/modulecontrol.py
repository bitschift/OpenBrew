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

def set_temp(temp):
    target = temp
    while (read_temp() != target):
        if ((target - read_temp()) > 40):
            IO.output(18, True)
            sleep(5)
            IO.output(18, False)
        elif (target - read_temp() < 0):
            IO.output(18, False)
        else:
            IO.output(18, True)
            sleep(2)
            IO.output(18, False)
    IO.output(18, False)

def set_stir(speed):
    duty = speed
    s.start(float(duty))

if __name__ == "__main__":
    while(1):
        op = input('Enter command: ')
        if (op == 1):
            temp = input('Enter temp: ')
            set_temp(temp)
        if (op == 2):
            speed = input('Set stir speed: ')
            set_stir(speed)
        
