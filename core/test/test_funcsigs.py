"""
Test functionalities import funcsigs.py to extract functions signatures 
following PEP 362
"""

def test_signatures():
    from openalea.core.funcsigs import signature
    s = signature(f)
    p = s.parameters
    
    assert len(p)==4
    assert p.keys()==['a','b','args','kargs']
    assert [pi.kind for pi in p.values()]==[1,1,2,4]
    assert p['b'].default==2
    
    
def f(a,b=2,*args,**kargs):
    """
    f(a,b=2,*args,**kargs) => a+b
    """
    return a+b