from argparse import ArgumentParser
from openalea.release import install_formula, eggify_formula, build_formula
from openalea.release.uninstall import uninstall

def main():
    # options
    parser = ArgumentParser(prog='easy_pkg')
    parser.add_argument('command', type=str, default="install",
                         help='Command to launch. It can be "download", "install", "build", "eggify", "uninstall"')
    parser.add_argument('package', type=str, default="openalea",
                         help='Package to work with. It can be "openalea", "vplants", "alinea" or other classical package like "qt4", "rpy2", "cgal"...')

    parser.add_argument('--no-download',dest='dl' , default="False", help="Don't download any packages, just install the ones already downloaded")
    parser.add_argument('--no-install',dest='inst' , default="False", help="Download and unpack all packages, but don't actually install them.")
    parser.add_argument('--no-deps',dest='inst' , default="False", help="Don't install package dependencies.")
    
    parser.add_argument('--force-download', default="False", help="Download even if already downloaded.")
    parser.add_argument('--force-install', default="False", help="Install even if already installed.")
    parser.add_argument('--force-build', default="False", help="Build even if already built.")
    parser.add_argument('--force', default="False", help="Force all: download, install and build")
    
    parser.add_argument('--download-dir', default="", help="download package to DIR")
    parser.add_argument('--install-dir', default="", help="install package to DIR")
    parser.add_argument('--src-dir', default="", help="unpack archive to DIR")
    parser.add_argument('--build-dir', default="", help="build package to DIR")
    parser.add_argument('-d', '--dir', default=".", help="Working DIR in which package will be download, installed, unpacked, built...")
    
    args = parser.parse_args()

    package_name = args.package
    command = args.command
    
    if command == "install":
        install_formula(package_name)
    elif command == "download":
        print "todo"
        # install_formula(package_name)
    elif command == "build":
        build_formula(package_name)
    elif command == "eggify":
        eggify_formula(package_name)
    elif command == "uninstall":
        print "Uninstall All OpenAlea for the moment..."
        print "todo: uninstall just selected package"
        uninstall()    
    
if __name__ == '__main__':
    main()