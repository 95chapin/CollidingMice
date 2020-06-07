import numpy as np
import torch
import matplotlib.pyplot as plt
import math
import os

from dqnAgent import Agent
from collections import deque

from environment import envReset, envStep
from mice import getNumMice, getMouseActions, getConstantSize, getLocalPath, getTargetPath, getLoadFromFile, getLoadFromFile, saveParam
import torch.optim as optim

def load_checkpoint(model, optimizer, loss, filename) :
    start_epoch = 0
    if os.path.isfile(filename):
        print("=> loading checkpoint '{}'".format(filename))
        checkpoint = torch.load(filename)
        start_epoch = checkpoint['epoch']
        model.load_state_dict(checkpoint['model_state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        loss = checkpoint['loss']
        print("=> loaded checkpoint '{}' (epoch {})".format(filename, start_epoch))
    else:
        print("=> no checkpoint found at '{}'".format(filename))
        
    return model, optimizer, start_epoch, loss

torch.manual_seed(0)

LR = 5e-4               # learning rate

constant = getConstantSize()    # Preprended state values
# numMice = 1   # numMice *2 = suffix state values
stateSize = constant + 2*getNumMice()
# actionOptions = [-60.0,-45.0, -30.0, -15.0, 0.0, 15.0, 30.0, 45.0, 60.0]
# actionOptions = [-45.0, -30.0, -15.0, 0.0, 15.0, 30.0, 45.0]
actionOptions = getMouseActions()

episodes = 10000

agent = Agent(state_size = stateSize, action_size = len(actionOptions), seed = 0)
if(getLoadFromFile() == True) :
    # checkpoint = torch.load(getLocalPath())
    # agent.qnetwork_local.load_state_dict(checkpoint['model_state_dict'])
    # agent.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    # lastEpisode = checkpoint['epoch']
    # agent.loss = checkpoint['loss']
    # agent.qnetwork_target.load_state_dict(torch.load(getTargetPath()))
    # agent.qnetwork_local.train()
    # agent.qnetwork_target.train()
    
    
    agent.qnetwork_local , agent.optimizer, lastEpisode, agent.loss = load_checkpoint(agent.qnetwork_local,agent.optimizer,agent.loss,getLocalPath())
    agent.qnetwork_target, agent.optimizer, lastEpisode, agent.loss = load_checkpoint(agent.qnetwork_target,agent.optimizer,agent.loss,getTargetPath())
    print("lastEpisode", lastEpisode)
    agent.qnetwork_local.train()
    agent.qnetwork_target.train()
else :
    lastEpisode = 0
    

        
def dqn(n_episodes = episodes, max_t = 1000, eps_start = 1.0, eps_end = 0.01, eps_decay = 0.996) :
    if(getLoadFromFile() == False) :
        with open(getLocalPath(), "a+") as f:
            print("Created : ", getLocalPath())
            
        with open(getTargetPath(), "a+") as f:
            print("Created : ", getTargetPath())
    # Deep Q-Learning
    
    # Params
    # n_episodes (int) : maximum number of training episodes
    # max_t (int) : maximum number of timestpes per episode
    # eps_start (float) : starting value of epsilon, for epsilon-greedy action selection
    # eps_end (float) : minimum value of epsilon
    # eps_decay (float) : multiplicative facot (per episode) for decreasing epsilon

    
    # Init score and eps
    scores = []                         # list containing score from each episode
    scores_window = deque(maxlen=200)   # last 100 scores
    eps = eps_start
    
    # Get the Qt running by initializing values 
    state = envReset()

    # Begin training
    for i_episode in range(1, n_episodes+1):
        state = envReset()  # Restart the environment
        score = 0           # Init score to zero
        
        for t in range(max_t):
            actionIndex = agent.act(state,eps)
            action = actionOptions[actionIndex]
            next_state, reward, done = envStep(action)
            agent.step(state, actionIndex, reward, next_state, done)
            
            # Above step decides whether we will train(learn) the network
            # Actor (local_qnetwork) or we will fill the replay buffer
            # if len replay buffer is equal to the batch size then we ill
            # train the network or otherwise we will add experience tuple in our 
            # replay buffer
            state = next_state
            score += reward
            
            if done:
                break
            
            print(done)
            scores_window.append(score)         # save the most recent score
            scores.append(score)                # Save the mose recent score
            eps = max(eps*eps_decay, eps_end)   # Decrease the epsilon
            # print('\rEpisode {}\tAverage Score {:.2f}'.format(i_episode,np.mean(scores_window)), end="")
            if i_episode %100==0:
                with open("avgScore.txt",'a+') as f:
                    f.write('\rEpisode {}\tAverage Score {:.2f}'.format(i_episode,np.mean(scores_window)))
                    
                # Save every 100
                # with open("avgScore.txt",'a+') as f:
                #     f.write('\nEnvironment solve in {:d} epsiodes!\tAverage score: {:.2f}'.format(i_episode-100, np.mean(scores_window)))
                #     torch.save(agent.qnetwork_local.state_dict(), 'checkpoint.pth')
                #     print("saved to checkpoint.pth")
                
            if np.mean(scores_window)>= 5.0: 
                with open("avgScore.txt",'a+') as f:
                    f.write('\nEnvironment solve in {:d} epsiodes!\tAverage score: {:.2f}'.format(i_episode-100, np.mean(scores_window)))

                with open(getLocalPath(), 'w') as f:
                    torch.save(agent.qnetwork_local.state_dict(), getLocalPath())
                    torch.save({'epoch': i_episode + lastEpisode,'model_state_dict': agent.qnetwork_local.state_dict(),
                                'optimizer_state_dict': agent.optimizer.state_dict(),
                                'loss': agent.loss}, getLocalPath())
                    print("i_episode: ",i_episode+ lastEpisode, " saved : ", getLocalPath())
                    
                with open(getTargetPath(), 'w') as f:
                    torch.save(agent.qnetwork_target.state_dict(), getTargetPath())
                    torch.save({'epoch': i_episode + lastEpisode,'model_state_dict': agent.qnetwork_target.state_dict(),
                                'optimizer_state_dict': agent.optimizer.state_dict(),
                                'loss': agent.loss}, getTargetPath())
                    print("i_episode: ",i_episode+ lastEpisode, " saved : ", getTargetPath())
                    
                saveParam(agent.qnetwork_target.fc1, "fc1")
                saveParam(agent.qnetwork_target.fc2, "fc2")
                saveParam(agent.qnetwork_target.fc3, "fc3")
                
                
                break
            
        # print("Episode: ", i_episode)
    print("i_episode ",i_episode)
    return scores
    
scores = dqn(episodes)
print("Done Training")
# Plot the scores
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(np.arange(len(scores)), scores)
plt.ylabel('Score')
plt.xlabel('Episode #')
plt.show()
            
            
            
            
            