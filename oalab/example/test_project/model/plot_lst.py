"""
input=lst,x_label="X",y_label="Y",z=0,sleep_time=0
output=lst
"""

from time import sleep
from pylab import plot, xlabel, ylabel, clf

sleep(int(sleep_time))
clf()
plot(lst)
xlabel(x_label)
ylabel(y_label)

