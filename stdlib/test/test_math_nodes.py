from openalea.core.alea import run
from openalea.core.pkgmanager import PackageManager
from random import random,randint
import unittest
import math

""" A unique PackageManager is created for all test of dataflow """
pm = PackageManager()
pm.init(verbose=False)
 
def test_add():
    """ Test of node + """
    res = run(('openalea.math','+'),inputs={'a':1,'b':2},pm=pm)  
    assert res[0] == 3


def function_tst(function_name, val1, res=True, arg1name='a'):
    """ Function test """
    epsilon = 1e-15
    rres = run(('openalea.math',function_name),inputs={arg1name:val1},pm=pm)  
    if (rres[0] - res) > epsilon :
        raise ValueError("Bad result for operator '"+function_name+"' with values "+str((val1))+'. Expected '+str(res)+', Got '+str(rres[0])+'.')
    
def binary_tst(opname, val1, val2, res = True, arg1name = 'a',arg2name = 'b'):
    """ Binary Test """
    rres = run(('openalea.math',opname),inputs={arg1name:val1,arg2name:val2},pm=pm)  
    if rres[0] != res :
        raise ValueError("Bad result for operator '"+opname+"' with values "+str((val1,val2))+'. Expected '+str(res)+', Got '+str(rres[0])+'.')
    
def test_eq():
    """ Test of equal operators """
    val1,val2 = random()*10000, random()*10000
    binary_tst('!=',val1,val2,val1!=val2)
    binary_tst('!=',val1,val1,False)
    binary_tst('==',val1,val2,val1==val2)
    binary_tst('==',val1,val1,True)
    val1,val2 = randint(0,10000), randint(0,10000)
    binary_tst('!=',val1,val2,val1!=val2)
    binary_tst('!=',val1,val1,False)
    binary_tst('==',val1,val2,val1==val2)
    binary_tst('==',val1,val1,True)

def test_sup():
    """ Test of sup operators """
    val1 = random()*10000
    val2 = val1 + (random()*10000)+1
    binary_tst('>',val1,val2,False)
    binary_tst('>',val2,val1,True)
    binary_tst('>',val1,val1,False)
    binary_tst('>=',val1,val2,False)
    binary_tst('>=',val2,val1,True)
    binary_tst('>=',val1,val1,True)
    val1 = randint(0,10000)
    val2 = val1 + randint(0,10000)+1
    binary_tst('>',val1,val2,False)
    binary_tst('>',val2,val1,True)
    binary_tst('>',val1,val1,False)
    binary_tst('>=',val1,val2,False)
    binary_tst('>=',val2,val1,True)
    binary_tst('>=',val1,val1,True)
    
def test_inf():
    """ Test of inf operators """
    val1 = random()*10000
    val2 = val1 + (random()*10000)+1
    binary_tst('<',val1,val2,True)
    binary_tst('<',val2,val1,False)
    binary_tst('<',val1,val1,False)
    binary_tst('<=',val1,val2,True)
    binary_tst('<=',val2,val1,False)
    binary_tst('<=',val1,val1,True)
    val1 = randint(0,10000)
    val2 = val1 + randint(0,10000)+1
    binary_tst('<',val1,val2,True)
    binary_tst('<',val2,val1,False)
    binary_tst('<',val1,val1,False)
    binary_tst('<=',val1,val2,True)
    binary_tst('<=',val2,val1,False)
    binary_tst('<=',val1,val1,True)
   

def test_binaries():
    """ Test of %""" 
    val1 = randint(0,10000)
    val2 = randint(1,5) 
    val1 *= val2
    # val1 is guaranteed to be a multiple of val2, so the following test must 
    # always return 0.
    binary_tst('%', val1, val2, 0)
    binary_tst('*', 2, 3, 6)
    binary_tst('+', 2, 3, 5)
    binary_tst('-', 2, 3, -1)
    binary_tst('/', 4, 2, 2)
    
def test_trigo():
    """ Test trigonometric functions """
    function_tst('cos', math.pi, -1)
    function_tst('sin', math.pi, 0.)
    function_tst('tan', math.pi, 0)
    function_tst('atan', math.pi/4.)
    function_tst('acos', -1, math.pi)
    function_tst('asin', -1, math.pi)

def test_others(): 
    binary_tst('cmp', 0, 1,-1)
    binary_tst('cmp', 1, 0,1)
    binary_tst('cmp', 1, 1,0)


if __name__=='__main__':
    test_eq()
    test_inf()
    test_sup()
    test_binaries()
    test_others()
    test_trigo()
