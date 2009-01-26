import os, sys
sys.path.append("..")
import version

filepattern = "../src/core"
outdir = "core-%s"%(version.version)

os.system('epydoc --html  -o %s %s'%(outdir, 'openalea.core'))
os.system('scp -r %s dufourko@scm.gforge.inria.fr:/var/lib/gforge/chroot/home/groups/openalea/htdocs/doc/openalea'%(outdir,))
os.system('ssh dufourko@scm.gforge.inria.fr "cd /var/lib/gforge/chroot/home/groups/openalea/htdocs/doc/openalea; ln -s %s core"'%(outdir))
