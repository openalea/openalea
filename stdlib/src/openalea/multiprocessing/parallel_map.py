from types import FunctionType

def parallel_map(function, seq):
    '''    
    '''
    from IPython.parallel import Client
    rc = Client() # remote client

    lview = rc.load_balanced_view()
    lview.block = True

    if function and seq:
        return ( lview.map(function, seq), )
    else:
        return ( [], )

