

import sys
import os
pj = os.path.join

for (ui, dst) in [ ('mainwindow.ui', pj('..','ui_mainwindow.py')),
                   ('newgraph.ui', pj('..','ui_newgraph.py')),
                   ('newpackage.ui', pj('..','ui_newpackage.py')),
                   ('tofactory.ui', pj('..','ui_tofactory.py')),
                   ('preferences.ui', pj('..','ui_preferences.py')),
                   ('ioconfig.ui', pj('..','ui_ioconfig.py')),
                   ('tableedit.ui', pj('..','ui_tableedit.py')),
                   ]:
    cmd = "pyuic4 %s > %s "%(ui, dst)
    print cmd
    os.system("pyuic4 %s > %s "%(ui, dst))



# resources 
os.system("pyrcc4 %s > %s "%("images.qrc", "..%simages_rc.py"%(os.sep,)))
