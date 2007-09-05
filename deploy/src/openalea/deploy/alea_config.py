# configure openalea environment variables


from openalea.deploy import check_system

def main():

    print "Execute the following code : \n"
    env = check_system()
    for k, v in env.items():
        print "export %s=%s\n"%(k, v)


if(__name__ == '__main__'):
    main()
