import os, sys
pj = os.path.join

from setuptools import setup


setup(
    name = 'OpenAlea.StdLib',
    version = '0.5.0' ,
    description = 'OpenAlea standard logical component library.', 
    long_description = '',
    author = 'OpenAlea consortium',
    author_email = '',
    url = 'http://openalea.gforge.inria.fr',
    license = 'Cecill-C',


    namespace_packages=['openalea'],
    create_namespaces=False,
    zip_safe=False,

    packages=['openalea.color', 'openalea.data',
              'openalea.csv', 'openalea.file',
              'openalea.functional',
              'openalea.math', 'openalea.model',
              'openalea.pickling', 'openalea.python',
              'openalea.string',
              'openalea.plotools',
              'openalea.image',
              'openalea.stat',
              'openalea.spatial',
              'openalea.stand',
              ],

    package_dir={"":"src" },

    # Dependencies
    setup_requires = ['openalea.deploy'],
    install_requires = ['openalea.core'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {
        "wralea": ['openalea.color = openalea.color', 
                   'openalea.data = openalea.data',
                   'openalea.csv = openalea.csv', 
                   'openalea.file = openalea.file',
                   'openalea.functional = openalea.functional',
                   'openalea.math = openalea.math', 
                   'openalea.model = openalea.model',
                   'openalea.pickling = openalea.pickling', 
                   'openalea.python = openalea.python',
                   'openalea.string = openalea.string',
                   'openalea.plotools = openalea.plotools',
                   'openalea.image = openalea.image',
                   'openalea.stat = openalea.stat',
                   'openalea.spatial = openalea.spatial',
                   'openalea.stand = openalea.stand',
                   

                   # Deprecated
                   'catalog.color = deprecated', 
                   'catalog.data = deprecated',
                   'catalog.csv = deprecated', 
                   'catalog.file = deprecated',
                   'catalog.functional = deprecated',
                   'catalog.math = deprecated', 
                   'catalog.model = deprecated',
                   'catalog.pickling = deprecated', 
                   'catalog.python = deprecated',
                   'catalog.string = deprecated',
              ],

        },

                     
    )


