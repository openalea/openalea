import sys
from setuptools import setup
sys.path.append("src")
import visualea.metainfo as metainfo
from os.path import join as pj



from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in zip(metadata.keys(), metadata.values()):
    exec("%s = '%s'" % (key, value))

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
    url=url,
    license=license,
    keywords='visual programming',

    # Packages
    py_modules = ['visualea_postinstall'],
    namespace_packages = ["openalea"],
    create_namespaces = True,
    
    packages = [pkg_name],
    package_dir = {pkg_name : pj('src', 'visualea'), '' : 'src', },
    include_package_data = True,
    zip_safe = False,
    
    # Scripts
    entry_points = { 'gui_scripts': [
                           'visualea = openalea.visualea.visualea_script:start_gui',
                           'aleashell = openalea.visualea.shell:main',

                           ]},

    postinstall_scripts = ['visualea_postinstall'],
    share_dirs = { 'share' : 'share' },
 
    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    install_requires = ['openalea.core'],

    )


