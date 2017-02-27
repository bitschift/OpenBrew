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
        self._mem_batch_size = 20
        self._default_reward = -0.1

    def _q_update(self, end_reward):
        '''
        Performs the Q-update on the neural network.
        This is done with the reward provided to the last state.
        '''
        if (len(self._memory) == 0):
            print("ERROR - Attempted to do Q-Learning with empty memory")
            return

        # randomly sample our experience replay memory
        replay_batch = random.sample(self._memory, self._mem_batch_size)
        x_train = []
        y_train = []

        for experience in replay_batch:
            #Get max_Q(S',a)
            old_state, action, reward, new_state = experience
            old_qval    = self._model.predict(np.array([old_state]), batch_size=1)
            new_q_value = self._model.predict(np.array([new_state]), batch_size=1)
            max_q_value = np.max(new_q_value)
            y = np.zeros((1, 3))
            y[:] = old_qval[:]

            # Update difference for non-terminal (if true)
            # and terminal (else) conditions.
            if reward == self._default_reward:
                update = (reward + (self._gamma * max_q_value))
            else:
                update = end_reward

            y[0][action] = update
            x_train.append(old_state)
            y_train.append(y.reshape(3,))

        x_train = np.array(x_train)
        y_train = np.array(y_train)

        self._model.fit(x_train,
                y_train,
                batch_size=self._mem_batch_size,
                nb_epoch=1,
                verbose=1
                )

    def _record(self, experience):
        '''
        Keep track of the history of the actions for experience replay
        the state info is: (state_t, action_t, reward_t, state_tt)
        '''
        self._memory.append(experience)
        if len(self._memory) > self._max_mem:
            del self._memory[0]

    def get_action(self, temperature, co2, gravity, time):
        '''
        Calculate an action for a given sensor state.
        This is the main interface for the AI during the brewing run.
        '''
        state = np.array([[temperature, co2, gravity, time]])
        q = self._model.predict(state, batch_size=1)
        return np.argmax(q)

    def batch_train(self, data_batch, actions, reward):
        '''
        By using a predetermined database of actions (simulated or real),
        train the Q-net.
        '''
        if (len(data_batch)) != len(actions):
            print("ERROR: Mismatch in dimensions of the data and action sets")
            print("       dim(data): ", len(data_batch), " dim(action): ", len(actions))
            return

        for i in range(len(data_batch)-2):
            experience = (data_batch[i], actions[i], self._default_reward, data_batch[i+1])
            print("experience: ", experience)
            self._record(experience)
        # build the last experience manually
        experience = (data_batch[-2], actions[-1], reward, data_batch[-1])
        self._record(experience)
        # train
        self._q_update(reward)






if __name__ == "__main__":
    # Make test agent
    agent = LearningAgent()
    states = [[30,10,50,1],
              [30,10,50,2],
              [30,10,50,3],
              [30,10,50,4],
              [30,10,50,5],
              [30,10,50,6],
              [30,10,50,7],
              [30,10,50,8],
              [30,10,50,9],
              [30,10,50,10],
              [32,11,60,11],
              [33,12,60,12],
              [34,15,65,13],
              [34,15,65,14],
              [34,16,67,15],
              [34,16,70,16],
              [34,18,73,17],
              [34,18,78,18],
              [33,18,79,19],
              [32,18,80,20],
              [31,16,80,21],
              [31,16,80,22],
              [31,14,80,23],
              [30,13,80,24],
              [30,13,80,25]]
    original_actions = []
    new_actions = []
    for s in states:
        original_actions.append(agent.get_action(s[0],s[1],s[2],s[3]))

    reward = 50
    agent.batch_train(states, original_actions, reward)
    for s in states:
        new_actions.append(agent.get_action(s[0],s[1],s[2],s[3]))
    print("old", original_actions)
    print("new", new_actions)



