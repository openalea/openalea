"""pybase node Tests"""

__license__ = "Cecill-C"
__revision__ = " $Id: test_pybase_node.py 1586 2009-01-30 15:56:25Z cokelaer $"

from openalea.core.alea import run
from openalea.core.pkgmanager import PackageManager


""" A unique PackageManager is created for all test of dataflow """
pm = PackageManager()
pm.init(verbose=True)


def test_read_csv_from_file():
    """ Test of node read_csv_from_file """
    res = run(('openalea.csv', 'read_csv_from_file'),\
        inputs={'filename': 'data/test.csv', 'delimiter': ' ', 'header': False}, pm=pm)

    res = run(('openalea.csv', 'read_csv_from_file'),\
        inputs={'filename': 'data/stand_data.csv', 'delimiter': ',', 'header':True}, pm=pm)

    res = run(('openalea.csv', 'read_csv_from_file'),\
        inputs={'filename': 'data/test2.csv', 'delimiter': ' '}, pm=pm)


test_read_csv_from_file()
