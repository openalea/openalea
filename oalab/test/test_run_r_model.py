
from openalea.oalab.model.r import RModel


def test_rmodel_io():
    code = """
    #input = lst
    #output = s
    
    s = sum(lst)
    """

    m = RModel(code=code)
    res = m.run([1, 2, 3])
    assert res[0] == 6  # get first element as integers are converted to arrays
