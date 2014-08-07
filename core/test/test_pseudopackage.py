__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.pkgmanager import PseudoPackage, PseudoGroup


def test_pseudopkg():
    """Test pseudo package"""
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

        assert p['A'][str(id(va))] == va
        assert p['B']['A'][str(id(vba))] == vba
        assert p['A']['E'][str(id(vae))] == vae
        assert p['A']['B'][str(id(vab))] == vab
        assert p['A']['B']['D'][str(id(vabd))] == vabd
        assert p['A']['B']['C'][str(id(vabc))] == vabc
