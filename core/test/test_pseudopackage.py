
from openalea.core.pkgmanager import PseudoPackage, PseudoGroup


def test_pseudopkg():
    
    for p in PseudoGroup("Test"), PseudoPackage("Test"):

        p.add_name("A.B.C", "ABC")
        p.add_name("A.B.D", "ABD")
        p.add_name("A.B", "AB")
        p.add_name("A.E", "AE")
        p.add_name("B.A", "BA")
        p.add_name("A", "A")
        
        assert p['A'][None] == 'A'
        assert p['B']['A'][None] == 'BA'
        assert p['A']['E'][None] == 'AE'
        assert p['A']['B'][None] == 'AB'
        assert p['A']['B']['D'][None] == 'ABD'
        assert p['A']['B']['C'][None] == 'ABC'


    
