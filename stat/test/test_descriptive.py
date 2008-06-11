import openalea.stat.descriptive as descriptive

def test_list_log():
    y = [2.,3.3]
    x = descriptive.list_log(y)
    assert 0.693147 < x[0][0] < 0.693148 and 1.193922 < x[0][1] < 1.193923

def test_stat_summary():
    y = [2., 4., 5.6, 2.3]
    x = descriptive.StatSummary(y)
    assert 1.668082 < x['standard deviation'] < 1.668083 and  1.999999 < x['minimum'] < 2.000001 and 3.149999 < x['median'] < 3.16 and 5.599999 < x['maximum'] < 5.61 and 3.474999 < x['mean'] < 3.475001

def test_Corr():
    x = [3., 4., 2., 5.1]
    y = [2., 4., 5.6, 2.3]
    z = descriptive.Corr(x,y)
    assert -0.6110889 < z['Cor'] < -0.6110888

def test_Mean():
    y = [2., 4., 5.6, 2.3]
    x = descriptive.Mean(y)
    assert 3.474999 < x < 3.475001
    
def test_Median():
    y = [2., 4., 5.6, 2.3]
    x = descriptive.Median(y)
    assert 3.149999 < x < 3.16

def test_Mode():
    y = [2., 4., 2., 2.3]
    x = descriptive.Mode(y)
    assert 1.999999 < x['modal value'][0] < 2.000001 

def test_Var():
    y = [2., 4., 5.6, 2.3]
    x = descriptive.Var(y)
    assert 2.782499 < x < 2.782501

def test_Std():
    y = [2., 4., 5.6, 2.3]
    x = descriptive.Std(y)
    assert 1.668082 < x < 1.668083

def test_Freq():
    y = [2., 4., 2., 2.3]
    x = descriptive.Freq(y)
    assert x['counts'][0] == 2.0 and x['counts'][1] == 1.0 and x['counts'][2] == 1.0

def test_Density():
    y = [2., 4., 2., 2.3]
    x = descriptive.Density(y)
    a = descriptive.Mean(x['x'])
    b = descriptive.Mean(x['y'])
    assert x['n'] == 4 and 2.99 < a < 3.01 and 0.236823 < b < 0.236824


