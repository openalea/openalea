import openalea.stat.stattest as stattest

def test_chisqtest():
    x = [1.,2.,4.,5.,3.,6.,7.,2.,5.]
    y = [3., 8., 2., 10., 3., 15., 18., 8., 9.]
    z = stattest.chisqtest(x,y)
    assert z['X-squared'] == 45.0 and 0.144473 < z['p.value'] < 0.144474

def test_ttest():
    x = [1.,2.,4.,5.,3.,6.,7.,2.,5.]
    y = [3., 8., 2., 10., 3., 15., 18., 8., 9.]
    z = stattest.ttest(x,y)
    assert -2.347654 < z['t.statistic'] < -2.347653 and 0.032084 < z['p.value'] < 0.032085

def test_kstest1():
    x = [1.,2.,4.,5.,3.,6.,7.,2.,5.]
    y = [3., 8., 2., 10., 3., 15., 18., 8., 9.]
    z = stattest.kstest(x,y)
    assert -0.666667 < z['ks.statistic'] < -0.666666 and 0.018663 < z['p.value'] < 0.018664

def test_kstest2():
    x = [1.,2.,4.,5.,3.,6.,7.,2.,5.]
    z = stattest.kstest(x, cdf = 'norm', args = [4., 1.])
    assert 0.310583 < z['ks.statistic'] < 0.310584 and 0.143350 < z['p.value'] < 0.143351
