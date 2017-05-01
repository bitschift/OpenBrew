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
    with open(path, "r") as fifo:
        while True:
            for line in fifo.readlines():
                if line == "start":
                    return True
                print "ERROR: Non-start signal recieved while waiting for start"
                return False

def brew():
    '''
    A single run of the brewing loop
    '''
    path = "/tmp/btcomm.fifo"
    actions = []
    data = []
    while not wait_start():
        continue
    while True:
        print "getting action..."
        action = AI.get_action(dc.read_temp(), dc.read_co2(), 0, time.time())
        # Log information for next training run locally
        actions.append(action)
        state = (dc.read_temp(), dc.read_co2(), 0, time.time())
        data.append(state)
        print "action recieved"
        if action == 0:
            print "heating"
            mc.set_temp(50)
            time.sleep(300)
            mc.set_temp(0)
        elif action == 1:
            print "stirring"
            mc.set_stir(50)
            time.sleep(100)
            mc.set_stir(0)
        elif action == 2:
            break
    with open(path, "r") as fifo:
        for line in fifo.readlines():
            if line[0:5] == "reward":
                reward = float(line[6:])
                AI.batch_train(data, actions, reward)
                return
            print "[ERROR] non-reward signal received while waiting for reward."
            return

if __name__ == "__main__":
    AI = la.LearningAgent()
    print "Learning agent instantiated"
    while True:
        brew()
