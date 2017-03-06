import os
import glob
import sys
import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

def read_waterLevel():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 5)
    return distance

def read_temp():
    base_dir = '/sys/bus/w1/devices'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    
    catdata = subprocess.Popen(['cat', device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')

    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    
    equals_pos = lines[1].find('t=')
    
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def log_data(temp, waterLevel):
    conn = sqlite3.connect (dbname)
    curs = conn.cursor()

    curs.execute("INSERT INTO data (temp, waterLevel) VALUES(" + temp + ", " + waterLevel + ");")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    current_level = read_waterLevel()
    while(1):
        log_data(read_temp(), current_level - read_waterLevel())
        current_level = read_waterLevel()
        time.sleep(600)
        
