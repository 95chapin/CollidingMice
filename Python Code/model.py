# -*- coding: utf-8 -*-
"""
Created on Thu May 21 09:48:13 2020

@author: willi
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import mice
from mice import getNumMice, getMouseActions, getConstantSize, getNumNodes

numNodes = 40   # Approx less than 2*numinputs
constant = getConstantSize()    # Preprended state values
# numMice = 1    # numMice *2 = suffix state values
stateSize = constant + 2*getNumMice()
#stateSize = 23  # The input size. 3 + 10*2 = 23
# actionOptions = [-45.0, -30.0, -15.0, 0.0, 15.0, 30.0, 45.0]
actionOptions = getMouseActions()
actionSize = len(actionOptions)     # ?

class QNetwork(nn.Module) :
    # One layer
    def __init__(self, state_size, action_size, seed, fc1_unit= getNumNodes(), fc2_unit = getNumNodes()):
    
    # Two layers
    # def __init__(self, state_size, action_size, seed, fc1_unit= 64, fc2_unit = 64, fc3_unit = 64):
        # Initialize parameters and build model.
        # state_size (int) : Dimension of each state
        # action_size (int): Dimension of each action
        # seed (int)       : Random seed
        # fc1_unit (int)   : Number of nodes in first hidden layer
        # fc2_unit (int)   : Number of nodes in second hidden laye
        
        super(QNetwork, self).__init__()    #   Calls __init__ method of nn.Module class
        self.seed = torch.manual_seed(seed)
        self.fc1 = nn.Linear(state_size, fc1_unit)
        self.fc2 = nn.Linear(fc1_unit, fc2_unit)
        self.fc3 = nn.Linear(fc2_unit, action_size)
        
        # self.seed = torch.manual_seed(seed)
        # self.fc1 = nn.Linear(state_size, fc1_unit)
        # self.fc2 = nn.Linear(fc1_unit, fc2_unit)
        # self.fc3 = nn.Linear(fc2_unit, fc3_unit)
        # self.fc4 = nn.Linear(fc3_unit, action_size)
        
    def forward(self, x) :
        # x = state
        
        # Build a network that maps state -> action values
        
        # One layer
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
        
        # One layer leaky relu
        # x = F.leaky_relu(self.fc1(x))
        # x = F.leaky_relu(self.fc2(x))
        # return self.fc3(x)
        
        # Two layers
        # x = F.relu(self.fc1(x))
        # x = F.relu(self.fc2(x))
        # x = F.relu(self.fc3(x))
        # return self.fc4(x)
    
