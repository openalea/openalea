"""script to automatically generate epydoc documentation


"""
import os
import sys
sys.path.append(os.path.abspath("../src/visualea"))
# version is in the core module
sys.path.append(os.path.abspath("../src/core"))
import version

module='visualea'

filepattern = "../src/" + module
outdir = module + "-%s"%(version.version)

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
opt = ' '.join(epydoc_options.split())
run('epydoc %s -o %s %s  ' % (opt, outdir, '../src/'+module+'/*.py'),
    verbose=True, test=True)

# once done, we can scp the documentation
run('scp -r %s scm.gforge.inria.fr:/home/groups/openalea/htdocs/doc/'
    % (outdir), verbose=True, test=True)
