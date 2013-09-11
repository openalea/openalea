from argparse import ArgumentParser
from openalea.release import install_formula

def main():
    # options
    parser = ArgumentParser(prog='install_pkg')
    parser.add_argument('package', type=str, default="openalea",
                         help='Package to install. It can be "openalea", "vplants", "alinea" or other classical package like "qt4", "rpy2", "cgal"...')
                         
                  
    args = parser.parse_args()

    package_name = args.package
    install_formula(package_name)
    
if __name__ == '__main__':
    main()