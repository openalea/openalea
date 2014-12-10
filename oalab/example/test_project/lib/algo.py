"""
define f1 and f2
"""

print("load 'algo' module")

def f1(nb_step):
    return range(1,nb_step+1)

def f2(nb_step):
    lst=[]
    for i in range(int(nb_step)):
        lst.append((i+1)**2)

    return lst