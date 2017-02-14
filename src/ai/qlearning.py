'''
qlearning.py :: A simple implementation of Q-Learning using
a neural net approximator.
'''
import json
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Activation
from keras.optimizers import sgd

class LearningAgent:
    '''
    The LearningAgent class encapsulates the learning portion of the project.
    This class provides a standard interface that abstracts away the needs
    of Q-Learning, needing only test-sets which require new choices,
    and then a rating of that set later on for learning.
    '''
    def __init__(self):
        # Q-Learning net structure. Structure is hard coded for now, as 
        # incorporating a variable number of sensors is theoretically difficult
        self._model = Sequential()
        self._model.add(Dense(4, input_shape=(4,), activation='relu'))
        self._model.add(Dense(4, activation='relu'))
        self._model.add(Dense(3))
        self._model.compile(sgd(lr=.2), "mse")
        # Experience replay aspects
        self._memory = list()
        self._discount = .9
        self._max_mem = 11000

    def _q_update(self, rating):
        pass

    def _record(self, state_info, brew_finished):
        '''
        Keep track of the history of the actions for experience replay
        the state info is: (state_t, action_t, reward_t, state_tt)
        '''
        self._memory.append(state_info, brew_finished)
        if len(self._memory) > self._max_mem:
            del self._memory[0]


    def _get_state(self):
        # Currently not sure if this function will be necessary, thought it would be
        # initially
        pass


    def give_feedback(self, rating):
        '''
        Pass feedback to the learning agent about the previous run.
        Q-Learning occurs after this function is run.
        '''
        # Apply reward to action history
        # Perform Q-update on history
        # train on updated history


        

    def get_action(self, temperature, co2, gravity, time):
        '''
        Calculate an action for a given sensor state.
        This is the main interface for the AI during the brewing run.
        '''
        state = np.array([[temperature, co2, gravity, time]])
        q = self._model.predict(state)
        return np.argmax(q)

    def batch_train(self, data_batch):
        '''
        By using a predetermined database of actions (simulated or real),
        train the Q-net.
        '''
        pass

if __name__ == "__main__":
    # Make test agent
    agent = LearningAgent()
    print("test action: ", agent.get_action(50, 100, 1.3, 60))
