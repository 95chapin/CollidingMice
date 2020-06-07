from watchFile import watchFile
from readClear import readClear
from sendQtMessage import sendQtMessage
from splitReturnData import splitReturnData
from mice import getNumMice, getMouseActions, getConstantSize

pathToWatch = r"C:\Users\willi\Downloads\CalPoly\Spring_20\EE_509\Final_Project\dirwatch\qt"
QToutputFileName = r"C:\Users\willi\Downloads\CalPoly\Spring_20\EE_509\Final_Project\dirwatch\qt\qtout.txt"
pyOutoutFileName = r"C:\Users\willi\Downloads\CalPoly\Spring_20\EE_509\Final_Project\dirwatch\py\pyout.txt"
constant = getConstantSize()     # Preprended state values
# numMice = 1    # numMice *2 = suffix state values
numMice = getNumMice()
envShape = constant + 2*numMice
def envReset() :
    
    while True :
        sendQtMessage(pyOutoutFileName,"restart")       # Start the Qt program over and return the intial state
        watchFile(pathToWatch)                      # Wait for the file to update before returning
        data = readClear(QToutputFileName)          # Read, return, and clear contents of file
        
        
        if len(data) > 0 :
            break
    state, reward, done = splitReturnData(data, constant, numMice)  # Get state, reward, and done
   
    return state

def envStep(action) :
    action = str(action)
    while True : 
        sendQtMessage(pyOutoutFileName,action)       # Start the Qt program over and return the intial state
        watchFile(pathToWatch)                      # Wait for the file to update before returning
        data = readClear(QToutputFileName)          # Read, return, and clear contents of file
        
        
        if len(data) > 0 :
            break     
    state, reward, done = splitReturnData(data, constant, numMice)  # Get state, reward, and done
    # state = np.ndarray(shape =(1, envShape), dtype = float, buffer = state)  
    return state, reward, done

def envStop():
    sendQtMessage(pyOutoutFileName,"end")       # Start the Qt program over and return the intial state
    