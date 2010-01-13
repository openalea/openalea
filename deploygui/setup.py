# -*- coding: utf-8 -*-
__revision__ = "$Id$"

from setuptools import setup, find_packages
from os.path import join as pj
    

keywords = ['Graphical installer']


from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))



setup(
    # Metadata for PyPi
    name = name,
    version = version,
    author = authors,
    author_email = authors_email,
    description = description,
    license = license,
    keywords = keywords,
    url = url,

    namespace_packages = ["openalea"],

    py_modules = ['deploygui_postinstall'],
    packages = ["openalea", "openalea.deploygui"],
    package_dir = { 'openalea' : 'src/openalea', 'openalea.deploygui': 'src/openalea/deploygui', '':'src'  }, 
    include_package_data = True,
    zip_safe = False,

    share_dirs = { 'share' : 'share'},
    entry_points = {
              "gui_scripts": [
                 "alea_install_gui = openalea.deploygui.alea_install_script:main", ],
              },
    
    postinstall_scripts = ['deploygui_postinstall'],
    # Dependencies
    install_requires = ['OpenAlea.Deploy>=0.4.13'],
    dependency_links = ['http://gforge.inria.fr/frs/...?id=79'],

)
