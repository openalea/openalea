import os, sys
sys.path.append("..")
import version

filepattern = "../src/core"
outdir = "%s"%(version.version)

os.system('epydoc --html  -o %s %s'%(outdir, filepattern))
