def readClear(filePath) :
    with open(filePath, 'r+') as file: # Use file to refer to the file object
       data = file.read().splitlines()
       file.truncate(0) # need '0' when using r+
    return data

