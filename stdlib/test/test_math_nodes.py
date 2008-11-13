from openalea.core.alea import run
from openalea.core.pkgmanager import PackageManager
from random import random,randint

""" A unique PackageManager is created for all test of dataflow """
pm = PackageManager()
pm.init(verbose=False)
 
def test_add():
    """ Test of node + """
    res = run(('openalea.math','+'),inputs={'a':1,'b':2},pm=pm)  
    assert res[0] == 3

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
    
