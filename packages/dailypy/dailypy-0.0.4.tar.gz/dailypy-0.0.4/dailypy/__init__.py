import numpy as np 
import os, time 

# Data manipulate

class dm:
    def __init__(self):
        pass

    def saveNp(self, a, name, path='.'):
        np.save(os.path.join(path,name), a)

    def saveTxt(self, a, name, path='.'):
        np.savetxt(os.path.join(path,name)+'.txt', a)
    
    def saveArrows(self, a1, a2, name='cols'):
        a1a2 = np.stack((a1,a2), axis=1)
        self.saveTxt(a1a2, name)


class sm:
    '''
    String manipulation
    '''
    def __init__(self):
        pass 

    def timeString():
        '''
        Get the string of the current date & time.
        '''
        return time.strftime("%Y%m%d-%H%M%S")
