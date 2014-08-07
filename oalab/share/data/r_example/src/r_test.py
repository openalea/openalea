%load_ext rmagic
#%pylab inline

import numpy as np
import pylab
X = np.array([0,1,2,3,4])
Y = np.array([3,5,4,6,7])
#pylab.scatter(X, Y)

%Rpush X Y
result1 = %R lm(Y~X)$coef

Xr = X - X.mean(); Yr = Y - Y.mean()
slope = (Xr*Yr).sum() / (Xr**2).sum()
intercept = Y.mean() - X.mean() * slope
(intercept, slope)

result2 = %R resid(lm(Y~X)); coef(lm(X~Y))

print result1, result2
