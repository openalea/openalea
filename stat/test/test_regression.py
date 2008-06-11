import openalea.stat.regression as regression
import openalea.stat.descriptive as descriptive

def test_Glm():
    x = [1.,2.,4.,5.,3.,6.,7.,2.,5.]
    y = [3., 8., 2., 10., 3., 15., 18., 8., 9.]
    z = regression.Glm(x,y,'poisson')
    assert 1.046794 < z['Intercept'] < 1.046795 and 0.250368 < z['Slope'] < 0.250369

def test_linearregression():
    x = [1.,2.,4.,5.,3.,6.,7.,2.,5.]
    y = [3., 8., 2., 10., 3., 15., 18., 8., 9.]
    z = regression.linearregress(x,y)
    assert 0.469594 < z['intercept'] < 0.469595 and 2.050675 < z['pente'] < 2.050676 and 0.580578 < z['r2'] < 0.580579
