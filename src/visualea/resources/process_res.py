

import sys
import os


for (ui, dst) in [ ('mainwindow.ui', '../ui_mainwindow.py'),
                   ('newgraph.ui', '../ui_newgraph.py'),
                   ('newpackage.ui', '../ui_newpackage.py'),
                   ]:
    os.system("pyuic4 %s > %s "%(ui, dst))



# resources 
os.system("pyrcc4 %s > %s "%("images.qrc", "../images_rc.py"))
