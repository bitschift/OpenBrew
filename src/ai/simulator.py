class Simulator():
    '''
    This is the simulator, which calculates new states and keeps track
    of the reward inherehnt in the system.
    This simulator is not meant to be a realistic model of the fermentation
    process, but rather a simple examination/test sim of the learning agent.
    '''
    def __init__(self):
        self._reward = 0

    def _new_temp(self, state):
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

    def _new_CO2(self, state):
        temp, CO2, grav, time = state
        if time < 50:
            CO2 += 5
        else:
            CO2 -= 1
        return CO2

    def _new_grav(self, state):
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
            self._reward -= 5
        elif temp < 20:
            self._reward -= 2
        else:
            self._reward += 3

        if CO2 > 50:
            self._reward -= 1
        elif CO2 < 10:
            self._reward -= 3
        else:
            self._reward += 2

        if grav > 40:
            self._reward -= 2
        elif grav < 10:
            self._reward -= 1
        else:
            self._reward += 1

        if time > 50:
            self._reward += 3
        elif time > 20:
            self._reward += 1
        elif time > 10:
            self._reward += 2

    def reset(self):
        '''
        resets the simulator
        '''
        self._reward = 0

    def new_state(self, state, action):
        '''
        Takes the current state and action, performs calculations
        and produces the next state to the action taker.
        Incremental rewards are recorded internally until reset() is called.
        '''
        temp, CO2, grav, time = state
        temp = self._new_temp(state)
        CO2 = self._new_CO2(state)
        grav = self._new_grav(state)
        time += 1

        if action == 0:
            # activate heating element
            temp += 1
        elif action == 1:
            # stir --> increase brewing speed
            CO2 += 1
            grav += 1
        elif action == 3:
            # end brewing (handled outside this function)
            pass
        state = (temp, CO2, grav, time)
        self._calcStepReward(state)
        return state
