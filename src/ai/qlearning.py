'''
qlearning.py :: A simple implementation of Q-Learning using
a neural net approximator.
'''
import json
import numpy as np
import random
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
        # The history is the series of (state,action) tuples during the running of the epoch
        self._history = []
        self._gamma = 0.975
        # Experience replay aspects
        self._memory = list()
        self._discount = .9
        self._max_mem = 10000
        self._mem_batch_size = 500

    def _q_update(self, reward):
        # randomly sample our experience replay memory
        replay_batch = random.sample(self._memory, self._mem_batch_size)
        x_train = []
        y_train = []
        for experience in replay_batch:
            #Get max_Q(S',a)
            old_state, action, reward, new_state = experience
            old_qval = self._model.predict(old_state, batch_size=1)
            new_q_value = self._model.predict(new_state, batch_size=1)
            max_q_value = np.max(new_q_value)
            y = np.zeros((1, 4))
            y[:] = old_qval[:]
            if reward == -1: # non-terminal state
                update = (reward + (self._gamma * max_q_value))
            else: #terminal state
                update = reward
            y[0][action] = update
            x_train.append(old_state)
            y_train.append(y.reshape(4,))

        x_train = np.array(x_train)
        y_train = np.array(y_train)
        self._model.fit(X_train, y_train, batch_size=self._mem_batch_size, nb_epoch=1, verbose=1)
        state = new_state

    def _record(self, state_info, brew_finished):
        '''
        Keep track of the history of the actions for experience replay
        the state info is: (state_t, action_t, reward_t, state_tt)
        '''
        self._memory.append(state_info, brew_finished)
        if len(self._memory) > self._max_mem:
            del self._memory[0]

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
        q = self._model.predict(state, batch_size=1)
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
