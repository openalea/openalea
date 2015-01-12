"""
input=x,y,num=0
output=x,y
"""

from pylab import figure, plot

#fig = figure(num)
#ax = fig.add_subplot(111)
#ax.plot(x, y)

plot(x,y)

print ('plot on fig %d' %int(num))
