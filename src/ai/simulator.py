class Simulator():
    def __init__(self):
        self._reward = 0

    def _newTemp(self, state):
        temp, CO2, grav, time = state

        if time < 10:
            temp += 1
        elif time < 20:
            temp += 2
        elif time < 50:
            temp += 5
        elif time < 70:
            temp -= 2
        else:
            temp -= 1
        return temp

    def _newTime(self, state):
        time = state[3]
        return time+1

    def _newCO2(self, state):
        temp, CO2, grav, time = state
        if time < 50:
            CO2 += 5
        else:
            CO2 -= 1
        return CO2

    def _newGrav(self, state):
        temp, CO2, grav, time = state
        if time < 50:
            grav += 5
        else:
            grav += 1
        return grav 

    def getReward(self):
        '''
        Returns the reward from the entire run
        '''
        return self._reward

    def _calcStepReward(self, state):
        '''
        calculates the differential reward for this time slice
        '''
        temp, CO2, grav, time = state
        if temp > 100:
            self._reward -= 


    def reset(self):
        '''
        resets the simulator
        '''
        self._reward = 0

    def newState(self, state, action):
        '''
        Takes the current state and action, performs calculations
        and produces the next state to the action taker.
        Incremental rewards are recorded internally until reset() is called.
        '''

