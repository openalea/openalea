====== OpenAlea.Deploy ======

**Authors** : S. Dufour-Kowalski 

**Contributors** : OpenAlea Consortium

**Institutes** : INRIA/CIRAD/INRA

**Type** : Pure Python package

**Status** : Devel

**License** : CeCILL-C


===== About =====

OpenAlea.Deploy support the installation of OpenAlea packages via the network and manage 
their dependencies .
It is an extension of [[http://peak.telecommunity.com/DevCenter/setuptools|Setuptools]].

**Additional Features** :
   * Discover and manage packages in EGG format
   * Declare shared libraries directory and include directories
   * Call SCons scripts
   * Create namespaces if necessary
   * Support post_install scripts
   * Support 'develop' command
   * OpenAlea GForge upload 

It doesn't include any GUI interface (See [[packages:compilation_installation:deploygui:deploygui|OpenAlea.DeployGui]] for that).

==== Requirements ====

  * [[http://www.python.org|Python >= 2.4]]
  * [[http://peak.telecommunity.com/DevCenter/setuptools|Setuptools]]

==== Download ====

See the [[:download|Download page]].

==== Installation ====

  python setup.py install

Note : OpenAlea.Deploy can be automatically installed with the //alea_setup.py// script.





==== Developper Documentation ====

To distribute your package with OpenAlea.Deploy, you need to write a setup.py script
as you do with setuptools.

  * have a look to the [[http://peak.telecommunity.com/DevCenter/setuptools|Setuptools developer's.
guide]].
  * OpenAlea.Deploy add a numerous of keywords and commands

=== Setup keywords ===

  * create_namespace = [True|False] : if //True// create the namespaces in //namespace_packages//
  * scons_scripts = [//list of Scons scripts//] : if not empty, call scons to build extensions
  * scons_parameters = [//list of Scons parameters//] : such as ''build_prefix=...''
  * postinstall_scripts = [//list of strings//] : Each string corresponds to a python module to execute at installation time. The module may contain a install function ''def install():''.
  * inc_dirs = {//dict of dest_dir:src_dir//} : Dictionary to map the directory containing the header files.
  * lib_dirs = {//dict of dest_dir:src_dir//} : Dictionary to map the directory containing the dynamic libraries to share.
  * share_dirs = {//dict of dest_dir:src_dir//} : Dictionary to map the directory containing shared data.

=== Additional setup.py commands ===

   * //create_namespace// : create_namespace declared in //namespace_packages//usage : ''python setup.py create_namespace''.
   * //scons// : call scons scripts, usage : ''python setup.py scons''.
   * //alea_install// : wrap easy_install command, usage : ''python setup.py alea_install''.
   * //alea_upload// : upload distribution forge on the openalea gforge

For more information see : ''python setup.py --help-commands''

=== Setup.py example ===

<code python>
import sys
import os
from setuptools import setup, find_packages
from os.path import join as pj

build_prefix = "build-scons"

# Setup function
setup(
    name = "OpenAlea.FakePackage",
    version = "0.1",
    author = "Me",
    author_email = "me@example.com",
    description = "This is an Example Package",
    license = 'GPL',
    keywords = 'fake',
    url = 'http://myurl.com',

    # Scons
    scons_scripts = ["SConstruct"],
    scons_parameters = ["build_prefix=%s"%(build_prefix)],

    # Packages
    namespace_packages = ["openalea"],
    create_namespaces = True,
    packages = ['openalea.fakepackage', ],
    
    package_dir = { 
                'openalea.fakepackage':  pj('src','fakepackage'), 
                '' : 'src',  # necessary to use develop command
                  }, 
    include_package_data = True,
    zip_safe= False,

    # Specific options of openalea.deploy
    lib_dirs = { 'lib' : pj(build_prefix, 'lib'), },
    inc_dirs = { 'include' : pj(build_prefix, 'include') },
    share_dirs = { 'share' : 'share' },
    postinstall_scripts = ['openalea.fakepackage.postinstall',],
    
    # Scripts
    entry_points = { 'console_scripts': [
                           'fake_script = openalea.fakepackage.amodule:console_script', ],
                     'gui_scripts': [
                           'fake_gui = openalea.fakepackage.amodule:gui_script',]},

    # Dependencies
    setup_requires = ['openalea.deploy'],
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],
    #install_requires = [],
    
)

</code>


