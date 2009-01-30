#!/usr/bin/python
"""script to automatically generate epydoc documentation"""
__revision__="$Id: gendoc.py 1582 2009-01-30 14:46:42Z cokelaer $"

import os


# Do not need the PDF or SCP options.
os.system("python ../../misc/gendoc.py -v -d ../../ -m deploy --skip-scp --skip-pdf")
