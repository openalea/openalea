""" alea config 

Update all the shared libraries in the openalea global share lib directory.
Try to update environment variable by:
- changing PATH value from the registry in Windows
- Create a new file in /etc/profile.d or .bashrc.
The global shared dir can be set by this command.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

from install_lib import get_default_dyn_lib, get_dyn_lib_dir
# from util import check_system
from command import set_env

from optparse import OptionParser
    
def main():
    """ todo """

    # options
    parser = OptionParser()
    parser.add_option( "--install-dyn-lib", dest="lib_dir",
                       help="Set the dynamic library path",
                       default=None)

    parser.add_option( "--print-dyn-lib", action="store_true", 
                       dest="printdir", default=False,
                       help="Show dynamic lib directory",)

    (options, args) = parser.parse_args()

    if(options.printdir):
        print get_dyn_lib_dir()

    if(options.lib_dir or not options.printdir):
        set_env(options.lib_dir)

#     env = check_system()

#     if('posix' in os.name):
#         for k, v in env.items():
#             print "export %s=%s\n"%(k, v)
            
#     elif('win' in sys.platform):
#         for k, v in env.items():
#             print "set %s=%s\n"%(k, v)





if(__name__ == '__main__'):
    main()
