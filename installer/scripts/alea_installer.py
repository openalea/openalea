#!/usr/bin/python

"""
alea_installer.py is a script allowing to install openalea packages

usage :
alea_installer.py  [-c] [-u url] package_names

-c     : (Re)configure OpenAlea. Warning : previous installed packages
          will be not removed.
-u url : specify the ressource url containing packages description.
         if url is not specified, use default url.
         
package_names : list of package to install (and their dependencies).
"""

DEFAULT_URL = "http://openalea.gforge.inria.fr/distributions/latest.xml"

import sys

def installation(distrib_url, package_names):
    """ Install packages
    @param distrib url is the distribution file
    """

    # Get distribution file
    print "Retrieving distribution description file.\n"
    
    from urllib import urlopen
    try:
        distrib_file = urlopen(distrib_url)
    except IOError:
        print "Cannot access to %s. Abording...\n"%(distrib_url)
        sys.exit()

    from openalea.installer import install
    install.start(distribfile, package_names)


def configure():
    """ Configure OpenAlea """

    from openalea.installer import config
    config.start()
    print "OpenAlea configuration has been done successfully."


def main():
    # Parse command line options
    url = DEFAULT_URL
    names = []
    force_configure = False
    
    from optparse import OptionParser

    parser = OptionParser()
    parser.set_description("alea_installer.py is a script allowing to install openalea packages")
    parser.set_usage("alea_installer.py  [-c] [-u url] package_names")
    parser.add_option( "-c", dest="config", action="store_true",
                  help="(Re)configure OpenAlea. Warning : previous installed packages" +\
                       "will be not removed.")
    parser.add_option( "-u", dest="url",
                  help="Specify the ressource url containing packages description")
    (options, args)= parser.parse_args()
    url = options.url or DEFAULT_URL
    names = args
    force_configure = options.config
    
    # Check OpenAlea configuration
    try:
        import openalea.config
    except :
        print "OpenAlea is not configured."
        force_configure = True

    if(force_configure): configure()
    
    # Start Installation
    installation (url, names)
    

if( __name__ == '__main__' ):
    main()
