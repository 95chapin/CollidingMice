import numpy as np
import random
from random import choice
from collections import namedtuple, deque

# Importing the model (function approximator for Q-table)
from model import QNetwork

import torch
import torch.optim as optim
import torch.nn.functional as F

from torch.autograd import Variable
from mice import getLocalPath, getTargetPath, getBatchSize

BUFFER_SIZE = int(1e5)  #replay buffer size
BATCH_SIZE = getBatchSize()         # minibatch size
GAMMA = 0.99            # discount factor
TAU = 1e-3              # for soft update of target parameters
LR = 5e-4               # learning rate
UPDATE_EVERY = 4        # how often to update the network

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

class Agent():
    # Interacts with and learns from environment
    
    def __init__(self, state_size, action_size, seed) :
        # Initialize an Agent object
        
        # Params
        # state_size (int)  : dimension of each state
        # action_size (int) : dimension of each action
        # seed (int)        : random seed
        
        self.state_size  = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)
        self.loss = 0
        
        # Q- Network
        # if(getLoadFromFile() == True) :
        #     self.qnetwork_local.load_state_dict(torch.load(getLocalPath()))
        #     self.qnetwork_target.load_state_dict(torch.load(getTargetPath()))
        #     self.qnetwork_local.eval()
        #     self.qnetwork_target.eval()

        # else :       
        self.qnetwork_local  = QNetwork(state_size, action_size, seed).to(device)
        self.qnetwork_target = QNetwork(state_size, action_size, seed).to(device)

        self.optimizer = optim.Adam(self.qnetwork_local.parameters(), lr=LR)
        
        
        # Replay memory
        self.memory = ReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE, seed)
        
        # Initialize time step (for updating every UPDATE_EVERY steps)
        self.t_step = 0
        
    def step(self, state, action, reward, next_step, done) :
        # Save experience in replay memory
        self.memory.add(state, action, reward, next_step, done)
        
        # Learn every UPDATE_EVERY time stpes.
        self.t_step = (self.t_step+1) % UPDATE_EVERY
        if self.t_step == 0:
            # If enough samples are available in memory, get random subse and learn
            if len(self.memory)>BATCH_SIZE:
                experience = self.memory.sample()
                self.learn(experience, GAMMA)
    
    def act(self, state, eps = 0) :
        # Returns action for given state as per current policy
        
        # Params
        # state (array_like) : current state
        # eps (float): epsilon, for epsilon-greedy ction selection
        
        # state = torch.from_numpy(state).astype('float').unsqueeze(0).to(device)
        # state = float(state)
        # temp = []
        # for x in state:
        #     temp.append(float(x))
        # state = temp
        # state = np.array(state)
        # print(state)
        # state = Variable(torch.Tensor([state]), requires_grad=True)
        
        # action = torch.zeros([self.action_size], dtype=torch.float32)
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)
        self.qnetwork_local.eval()
        with torch.no_grad():
            action_values = self.qnetwork_local(state)
            # print(action_values)
        self.qnetwork_local.train()
        
        # action = np.argmax(action_values.cpu().data.numpy())
        
        # action = action_values.cpu().data.numpy()
        # action = np.argmax(action)
        # with open("decision.txt",'a+') as f:
        #     f.write(" NN Action: " + str(action))
        # return action

        # # Epsilon - greedy action selection
        if random.random() > eps:
            action = np.argmax(action_values.cpu().data.numpy())
            # action = np.asarray(np.expand_dims(state, axis=0) / self.state_size, dtype=np.float32)
            # action = self.qnetwork_local.get_q_action(sess, action)[0]
            #with open("decision.txt",'a+') as f:
            #    f.write(" NN Action: " + str(action))

            # print("NN: ",np.argmax(action_values.cpu().data.numpy()))
                # print(action)
            return action
        else:
            action = random.choice(np.arange(self.action_size))
            #with open("decision.txt",'a+') as f:
            #    f.write(" Random Action: " + str(action))
            
            # print("rand: ", random.choice(np.arange(self.action_size)))
            return action
         
    
    def learn(self, experiences, gamma): 
        # Update value parameters using given batch of experience tuples
        
        # Params
        # experiences (Tuple[torch.Variable]): tupple of (s, a, r, s', done) tuples
        # gamma (float) : discount factor
        
        states, actions, rewards, next_states, dones = experiences # next_states might be next_state. typo ?
        
        # TODO: compute and minimize the loss
        criterion = torch.nn.MSELoss()
        
        self.qnetwork_local.train()
        self.qnetwork_target.eval()
        
        # Shape of output from the model (batch_size, action_dim) - (64,4)   
        predicted_targets = self.qnetwork_local(states).gather(1, actions)
        # predicted_targets = self.qnetwork_local(states).gather(1, actions)
        
        #####################  ADD DDQN learning at this line
        self.qnetwork_local.eval()
        
        with torch.no_grad():
            # labels_next = self.qnetwork_target(next_states).detach().max(1)[0].unsqueeze(1) # replace this for DDQN 
            # labels_next = self.qnetwork_target(next_State).detach().max(1)[0].unsqueeze(1)
            actions_q_local = self.qnetwork_local(next_states).detach().max(1)[1].unsqueeze(1).long()
            labels_next = self.qnetwork_target(next_states).gather(1,actions_q_local)
        
        self.qnetwork_local.train()
        #####################  END ADD DDQN
        
        # .detach() -> Returns a new Tensor, detached from the current graph
        # Calc - Q-Values currents
        labels = rewards + (gamma* labels_next*(1-dones))
        
        # Compute loss
        self.loss = criterion(predicted_targets, labels).to(device)

        # https://medium.com/@david010/collecting-bananas-with-a-deep-q-network-26c7a45d4c27

        # Minimize loss
        self.optimizer.zero_grad()
        self.loss.backward()
        self.optimizer.step()
        # __________________  update target network ______________________#
        self.soft_update(self.qnetwork_local, self.qnetwork_target, TAU)
        
    def soft_update(self, local_model, target_model, tau):
        # Soft update model paramters
        # theta_target = tau*theta_local + (1 - tau)*theta_target
        
        # Params
        # local model (PyTorch model): weights will be copied from
        # target model (PyTorch model): weights will be copied to
        # tau (float): : interpolation parameter
        
        for target_param, local_param in zip(target_model.parameters(),
                                           local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1-tau)*target_param.data)

class ReplayBuffer:
        # Fixed - size buffer to store experience tuples
    def __init__(self, action_size, buffer_size, batch_size, seed):
        # Initialize a ReplayBuffer object.
        
        # Params
        # action_size (int): dimension of each action
        # buffer_size (int): maximum size of buffer
        # batch_size (int) : size of each training batch
        # seed (int) : random seed
        
        self.action_size = action_size
        self.memory = deque(maxlen = buffer_size)
        self.batch_size = batch_size
        self.experiences = namedtuple("Experience", field_names = ["state",
                                                                   "action",
                                                                   "reward",
                                                                   "next_state",
                                                                   "done"])
        self.seed = random.seed(seed)
        
    def add(self, state, action, reward, next_state, done) :
        # Add a new experience to memory
        e = self.experiences(state, action, reward, next_state, done)
        self.memory.append(e)
        
    def sample(self) :
        # Randomly sample a batch of experiences from memory
        experiences = random.sample(self.memory,k=self.batch_size)
        
        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
        
        return (states,actions,rewards,next_states,dones)
    
    def __len__(self) :
        # Return the current size of internal memory
        return len(self.memory)
        