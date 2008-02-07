
from openalea.core.pkgmanager import PseudoPackage, PseudoGroup


def test_pseudopkg():
    
    for p in PseudoGroup("Test"), PseudoPackage("Test"):

        va = "A"
        vabc = "A.B.C"
        vabd = "A.B.D"
        vab = "A.B"
        vae = "A.E"
        vba = "B.A"

        p.add_name("A.B.C", vabc)
        p.add_name("A.B.D", vabd)
        p.add_name("A.B", vab)
        p.add_name("A.E", vae)
        p.add_name("B.A", vba)
        p.add_name("A", va)
        
        
        assert p['A'][id(va)] == va
        assert p['B']['A'][id(vba)] == vba
        assert p['A']['E'][id(vae)] == vae
        assert p['A']['B'][id(vab)] == vab
        assert p['A']['B']['D'][id(vabd)] == vabd
        assert p['A']['B']['C'][id(vabc)] == vabc


    
