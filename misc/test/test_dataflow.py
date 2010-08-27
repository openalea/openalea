from openalea.core.alea import *

pm = PackageManager()
pm.init(verbose=False)

def test_shared_data_browser():
    res = run(('openalea.misc.test','shared_data_browser'),{},pm=pm)
    assert res == []

if __name__ == "__main__":
    test_demo_corsican()
    test_demo_dycorinia()
    test_stat_tool_tutorial_compound()
    test_stat_tool_tutorial_convolution()

