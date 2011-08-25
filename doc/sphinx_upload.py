from optparse import OptionParser
from setuptools import Command
from openalea.deploy import command
import subprocess
import os

__author__ = "Thomas Cokelaer"


def ParseParameters(check=True):
    """ type --help to get help   """

    usage = """Usage: %prog [options]

    Assuming you have your ssh key on the gforge, you can upload
    the html and latex directories of the main sphinx openalea
    documentation (in openalea/doc). Before you would have created
    the HTML and LaTeX outputs typing::

        make html
        make latex

    :Usage:

        python sphinx_upload --username your_username
    """
    parser = OptionParser(usage=usage, \
        version = "%prog SVN $Id$ \n" \
      + "$Name:  $\n"  + __author__)

    parser.add_option("-u", "--username", metavar='USERNAME',
        action="store",default=None,
        help="gforge username")

    parser.add_option("-U", "--unstable", metavar='UNSTABLE',
        action="store",default=True,
        help="Upload to unstable directory or not.")

    (opts, args)= parser.parse_args()
    return opts, args




if __name__=="__main__":

    (options, _dummy) = ParseParameters()
    if options.username == None:
        print '--username must be provided'
        import sys
        sys.exit()
    outputs = ['html', 'latex']
    for output in outputs:
        cwd = os.getcwd()
        # adapt the input argument to scp depending whether we are in  ./doc
        # or in the main openalea directory
        if cwd.endswith('doc'):
            prefix = '_build'
        else:
            prefix = os.path.join('doc', '_build')

        base = "beta_doc" if options.unstable else "doc"
        direc = '/home/groups/openalea/htdocs/%s/openalea/doc/_build'%base
        cmd0 = 'ssh %s@%s "if [ ! -d %s ]; then mkdir -p %s; fi;"' \
            %(options.username,
              'scm.gforge.inria.fr',
              direc,
              direc)

        print cmd0
        status = subprocess.call(cmd0 ,stdout=open('/tmp/test','w'),stderr=None, shell=True)

        cmd1 = 'scp -r %s %s@%s:%s/' \
                % ( os.path.join(prefix, output),
                    options.username,
                    'scm.gforge.inria.fr',
                    direc
                    )
        print cmd1
        try:
            status = subprocess.call(cmd1 ,stdout=open('/tmp/test','w'),stderr=None, shell=True)
        except:
            pass

        print "   %s done" % output
    print "Logout..."

