"""script to automatically generate epydoc documentation


"""
import os, sys
sys.path.append(os.path.abspath("../src/core"))
import version

filepattern = "../src/core"
outdir = "core-%s"%(version.version)
admin_name = 'cokelaer'


epydoc_options= """
--html
--name epydoc_test
--docformat restructuredtext
--graph all
--url http://openalea.gforge.inria.fr
--include-log
--show-sourcecode
"""

def run(cmd, verbose=True, test=True):
    if verbose:
        print cmd
    if not test: 
        os.system(cmd)


# this is the epydoc command line arguments
opt= ' '.join( epydoc_options.split() )
run(' epydoc %s -o %s %s  '%(opt, outdir, '../src/core/*.py'), verbose=True, test=True)

# once done, we can scp the documentation
#run('scp -r %s %s@scm.gforge.inria.fr:/var/lib/gforge/chroot/home/groups/openalea/htdocs/doc/'%(outdir,admin_name), verbose=True, test=True)
