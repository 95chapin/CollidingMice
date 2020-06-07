def sendQtMessage(filePath, message) :
    with open(filePath, 'w') as file: # Use file to refer to the file object
        file.write(message) 

