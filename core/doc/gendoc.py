import os, sys
sys.path.append(os.path.abspath("../src/core"))
import version

filepattern = "../src/core"
outdir = "core-%s"%(version.version)

os.system('epydoc --html  -o %s %s'%(outdir, '../src/core/*.py'))
os.system('scp -r %s dufourko@scm.gforge.inria.fr:/var/lib/gforge/chroot/home/groups/openalea/htdocs/doc/'%(outdir,))
os.system('ssh dufourko@scm.gforge.inria.fr "cd /var/lib/gforge/chroot/home/groups/openalea/htdocs/doc; ln -s %s core"'%(outdir))
