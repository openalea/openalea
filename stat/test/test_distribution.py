import openalea.stat.distribution as distribution
import openalea.stat.descriptive as descriptive

def test_random_continuous_law():
    y = distribution.random_continuous_law('norm',100000,[0,1])
    a = descriptive.Mean(y[0])
    b = descriptive.Var(y[0])
    assert -0.1 < a < 0.1 and 0.9 < b < 1.1

def test_dnorm():
    x = distribution.dnorm(3.,2., 5.)
    assert 0.078208 < x[0] < 0.078209

def test_pnorm():
    x = distribution.pnorm(3., 2., 5.)
    assert 0.5792597 < x[0] < 0.5792598

def test_dpois():
    x = distribution.dpois(3,1.2)
    assert 0.086743 < x[0] < 0.086744

def test_ppois():
    x = distribution.ppois(3,1.2)
    assert 0.966231 < x[0] < 0.966232

def test_random_law_discrete():
    y = distribution.random_discrete_law('geom', 100000, [0.2])
    a = descriptive.Mean(y[0])
    b = descriptive.Var(y[0])
    assert 3.9 < a < 4.1 and 19.5 < b < 20.5
