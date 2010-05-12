
def parallel_map(function, seq):
    '''    
    '''
    from IPython.kernel import client
    tc = client.TaskClient()
    if function and seq:
        return ( tc.map(function, seq), )
    else:
        return ( [], )

