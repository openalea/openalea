"""
from openalea.oalab.history.history import History

def test_create_and_reset():
    a = 1
    b = 2
    c = 3
    d = "Viva Virtual Plants Lab!!!"

    h = History()
    h.add("a",a)
    h.add("b",b)
    h.add("the_answer",42)
    h.reset()
    h.add("c",c)
    h.add("d",d)
    hist = h.getHistory()
    
    assert len(hist) == 2

    
"""
