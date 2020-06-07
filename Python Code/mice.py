import numpy
import torch

def getNumMice() :
    NUM_MICE = 1
    return NUM_MICE

def getMouseActions() :
    actionOptions = [315 ,345, 0, 15, 45]
    return actionOptions

def getConstantSize() :
    constantSize = 2
    return constantSize

def getLocalPath() :
    return 'checkpointLocal.pth'
    
def getTargetPath() :
    return 'checkpointTarget.pth'

def getLoadFromFile() :
    return True

def getBatchSize() :
    batchSize = 25
    return batchSize

def getNumNodes() :
    numNodes = 25
    return numNodes

def saveParam(modelNode, filename):
    filenamew = filename +"w.txt"
    with open(filenamew, '+a') as f:
        f.write(str(torch.sum(modelNode.weight.data).numpy()) +"\n")
    
    filenameb = filename +"b.txt"
    with open(filenameb, '+a') as f:
        f.write(str(torch.sum(modelNode.bias.data).numpy())+"\n")

def readParam(filename) :
    fw = []
    fb = []
    filenamew = filename +"w.txt"
    with open(filenamew, 'r') as f:
        w = f.readlines()
    for x in w:
        fw.append(float(x))
    
    filenameb = filename +"b.txt"
    with open(filenameb, 'r') as f:
        b = f.readlines()
    for x in b:
        fb.append(float(x))
        
    return fw, fb
    