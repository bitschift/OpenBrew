'''
This file uses the simple simulator in simulator.py to train
the Q-learning agent to make optimal decisions in the brewing process.
The initial state will be all zeros, as this should inspire an
initial action to increase the temperature.
'''
import simulator
import qlearning
import random

def get_action(alpha, agent, state):
    if random.random() < alpha:
        action = random.choice([0, 1])
    else:
        action = agent.get_action(state[0], state[1], state[2], state[3])
    return action

def run_trial(agent, sim):
    '''
    Uses an agent and a simulator to run a single brewing batch.
    Once the batch is done, traing occurs after this trial.
    '''
    state = (30, 20, 10, 0)
    alpha = .5
    brew_over = False
    max_time = 30

    states = []
    actions = []
    while not brew_over:
        action = get_action(alpha, agent, state)
        states.append(state)
        actions.append(action)
        if alpha != 0:
            alpha -= 0.05
        if action == 2 or state[3] == max_time:
            brew_over = True
            reward = sim.getReward()
        else:
            state = sim.new_state(state, action)
    print("Reward: ", reward, "\tActions taken: ", len(actions))
    reward_data.write(str(reward)+',')
    result = agent.batch_train(states, actions, reward)
    if result != None:
        return "ERROR"
    else:
        return None

if __name__ == '__main__':
    agent_instance = qlearning.LearningAgent()
    sim_instance = simulator.Simulator()
    num_trials = 5000
    i = 0

    reward_data = open("reward.csv", 'w')

    while i != num_trials:
        print("===== Trial: ", i, "=====")
        result = run_trial(agent_instance, sim_instance)
        if result is None:
            i += 1
        sim_instance.reset()
