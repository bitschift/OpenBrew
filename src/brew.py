import os
import glob
import sys
import time
import ai.qlearning as la
import hwctrl.datacollect as dc
import hwctrl.modulecontrol as mc

def wait_start():
    '''
    Waits for the start signal in the fifo,
    and then resumes execution of the rest of the program.
    '''
    path = "/tmp/btcomm.fifo"
    while True:
        for line in open(path, "r"):
            if (line == "start"):
                return True
            else:
                print "ERROR: Non-start signal recieved while waiting for start"
                return False

if __name__ == "__main__":
    ai = la.LearningAgent()
    print "Learning agent instantiated"
    while not wait_start():
        continue
    while(True):
        print "getting action..."
        action = ai.get_action(dc.read_temp(), dc.read_co2(), 0, time.time())
        print "action recieved"
        if (action == 0):
            print "heating"
            mc.set_temp(50)
            time.sleep(300)
            mc.set_temp(0)
        elif (action == 1):
            print "stirring"
            mc.set_stir(50)
            time.sleep(100)
            mc.set_stir(0)
        elif (action == 2):
            break
