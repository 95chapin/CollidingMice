import torch
from dqnAgent import Agent
from environment import envReset, envStep, envStop

import math
from mice import getNumMice, getMouseActions, getConstantSize, getLocalPath, getTargetPath
import time
 


# load the weight from file
constant = getConstantSize()    # Preprended state values
numMice = getNumMice()    # numMice *2 = suffix state values
stateSize = constant + 2*numMice
# actionOptions = [-45.0, -30.0, -15.0, 0.0, 15.0, 30.0, 45.0]
actionOptions = getMouseActions()
actionSize = len(actionOptions)
agent = Agent(state_size=stateSize,action_size=actionSize,seed=0)
checkpoint = torch.load(getLocalPath())
agent.qnetwork_local.load_state_dict(checkpoint['model_state_dict'])
agent.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
episodes = checkpoint['epoch']
agent.loss = checkpoint['loss']
agent.qnetwork_target.load_state_dict(torch.load(getTargetPath()))
agent.qnetwork_local.eval()
agent.qnetwork_target.eval()

print("Training episodes", episodes)

# watch an untrained agent
rewards = []
for i in range(100):
    state = envReset()
    
    for j in range(200) :
        action = agent.act(state)
        action = actionOptions[action]
        state, reward, done = envStep(action)
        # Wait for 5 seconds
        time.sleep(.006)
        if done == True :
            envReset()

    # if done:
    #     break

print(rewards)
envStop()
    
