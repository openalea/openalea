# configure openalea environment variables


from openalea.deploy import check_system

def main():

    env = check_system()
    for k, v in env.items():
        print "export %s=%s\n"%(k, v)


if(__name__ == '__main__'):
    main()
