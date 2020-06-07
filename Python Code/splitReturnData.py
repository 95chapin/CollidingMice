import numpy as np

def splitReturnData(data, constant, numAppend) :
    if constant == 1 :
        temp = data[1]
        data.remove(temp)
    
    temp = []
    for x in data:
        temp.append(float(x))
    data = temp
    data = np.array(data)


    
    # Remove angle from state with zero danger mice
    if constant == 1 :
        # endState = constant + 2*numAppend
        state = data[0]
        reward = data[1]
        done = data[2]
    else:
        endState = constant + 2*numAppend
        state = data[0:endState]
        reward = data[endState:endState + 1]
        done   = data[endState+1:len(data)]
    
    # state = np.ndarray(shape =(1, len(state)), dtype = float, buffer = state)
    # state = np.ndarray(shape =(1, len(state)), dtype = float, buffer = state)

    # reward = np.ndarray(shape =(1, len(reward)), dtype = float, buffer = reward)
    # done = np.ndarray(shape =(1, len(done)), dtype = float, buffer = done)
    
    # Convert done into boolean
    if int(done) == 0 :
        done = False
    elif int(done) == 1 :
        done= True
        
    return state, reward, done
    