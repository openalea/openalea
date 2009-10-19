from openalea.misc.multisetup import Multisetup

def multisetup(directory, command, in3, in4):
    '''    Multi Setup allows to build and install all the packages
    '''
    # write the node code here.
    mysetup = Multisetup(commands=command, packages=in3, curdir=directory, verbose=in4)
    	
    # return outputs
    try:
        mysetup.run(color=False)
        return True
    except:
        return False
   
    
