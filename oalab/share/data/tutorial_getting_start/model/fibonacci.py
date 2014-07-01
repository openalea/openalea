nb_step = 20

try:
    xi
except NameError:
    xi = 1
    xj = 1
    n = 2

def step():
    global xi, xj, n
    xk = xi + xj
    xi = xj
    xj = xk
    n = n + 1
    print "Value number", n, " : ", xj
    
def init():
    global xi, xj, n
    xi = 1
    xj = 1
    n = 2
    print "Value number", 1, " : ", xi    
    print "Value number", n, " : ",xj
    
def animate():
    for i in range(nb_step):
        step()
