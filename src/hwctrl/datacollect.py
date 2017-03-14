import os
import glob
import sys
import time

import RPi.GPIO as IO

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-0416935b62ff/w1_slave'

IO.setmode(IO.BCM)
IO.setup(21, IO.IN)

def read_co2():
    return IO.input(21)

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp = float(temp_string) / 1000.0
        return temp

def log_data(temp, waterLevel):
    conn = sqlite3.connect (dbname)
    curs = conn.cursor()

    curs.execute("INSERT INTO data (temp, waterLevel) VALUES(" + temp + ", " + waterLevel + ");")
    conn.commit()
    conn.close()

if __name__ == '__main__':
  #  current_level = read_co2()
  #  while(1):
  #      log_data(read_temp(), current_level - read_co2())
  #      current_level = read_co2()
  #      time.sleep(600)
  
  while(1):
    print(read_temp())
