import os
import glob
import sys
import time
import ai.qlearning as la
import hwctrl.datacollect
import hwctrl.modulecontrol

if __name__ == "__main__":
    while(1):
        action = la.get_action(get_temp(), get_waterlevel(), time.time())
        if (action == 1):
            set_stir(50)
            sleep(100)
            set_stir(0)
        if (action == 0):
            set_heat(50)
            sleep(300)
            set_heat(0)
        if (action == 2):
            sys.exit()
