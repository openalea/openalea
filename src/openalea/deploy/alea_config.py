# Configure openalea environment variables


from openalea.deploy import check_system
import os, sys

def main():

    env = check_system()

    if('posix' in os.name):
        for k, v in env.items():
            print "export %s=%s\n"%(k, v)
            
    elif('win' in sys.platform):
        for k, v in env.items():
            print "set %s=%s\n"%(k, v)

    


if(__name__ == '__main__'):
    main()
