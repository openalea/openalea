"""
This model compute the Fibonacci sequence in calling *fibo* model.

*fibo(xi,xj)* (with j=i+1) compute the Fibonacci number i+2.

input = nb_step=20
output = xj
"""

fibo = Model("fibo")

xi, xj = 1, 1
print(xi, xj)

for i in range(int(nb_step)-1):
    xi, xj = fibo(xi,xj)
    print (xj)
