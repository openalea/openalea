"""
  OpenAlea.Installer : Copyright 2006 CIRAD, INRIA
"""



from distutils.core import setup

description = "OpenAlea Installer"
author = "Samuel Dufour-Kowalski"
url = "http://openalea.gforge.inria.fr"
license = "Cecill-C"
version = '0.1'

# Distutils Setup function
setup(
    name = "OpenAlea.Installer",
    version = version,
    description = description,
    author = author,
    url = url,
    license = license,
    scripts = ['scripts/alea_installer.py'],
    packages = ['openalea', 'openalea.installer'],
    )


