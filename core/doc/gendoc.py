#!/usr/bin/python
"""script to automatically generate epydoc documentation"""
__revision__="$Id$"

import os


# Do not need the PDF or SCP options.
os.system("python ../../misc/gendoc.py -v -d ../../ -m core --skip-scp --skip-pdf")
