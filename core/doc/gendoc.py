import os, sys
sys.path.append(os.path.abspath("../src/core"))
import version

filepattern = "../src/core"
outdir = "core-%s"%(version.version)
admin_name = 'cokelaer'
def run(cmd, verbose=True, test=True):
    if verbose: print cmd
    if not test : os.system(cmd)



run('epydoc --html  -o %s %s --docformat restructuredText --include-log --show-sourcecode '%(outdir, '../src/core/*.py'), verbose=True, test=True)


run('scp -r %s %s@scm.gforge.inria.fr:/var/lib/gforge/chroot/home/groups/openalea/htdocs/doc/'%(outdir,admin_name), verbose=True, test=True)
#os.system('ssh %s@scm.gforge.inria.fr "cd /var/lib/gforge/chroot/home/groups/openalea/htdocs/doc; ln -s %s core"'%(outdir, admin_name))
