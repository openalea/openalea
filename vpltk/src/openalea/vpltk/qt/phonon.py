# -*- coding: utf-8 -*-

import os
import platform

if os.environ['QT_API'] == 'pyqt':
    if platform.system() == 'Darwin' and platform.mac_ver()[0].split('.')[:2] == ['10', '12']:
        # illegal instruction 4 on Mac Sierra using conda packages, so temporary disabling phonon
        pass
    else:
        from PyQt4.phonon import *
else:
    from PySide.phonon import *
