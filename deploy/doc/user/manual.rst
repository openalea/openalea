.. testsetup::

Developper Documentation
========================

To distribute your package with OpenAlea.Deploy, you need to write a setup.py script as you do with setuptools.
    * have a look to the Setuptools developer's. guide.
    * OpenAlea.Deploy add a numerous of keywords and commands

Setup keywords
--------------

* create_namespace = [True | False] : if *True* create the namespaces in *namespace_packages*
* scons_scripts = [*list of Scons scripts*] : if not empty, call scons to build extensions
* scons_parameters = [*list of Scons parameters*] : such as build_prefix = …
* postinstall_scripts = [*list of strings*] : Each string corresponds to a python module to execute at installation time. The module may contain a install function def install():.
* inc_dirs = {*dict of dest_dir:src_dir*} : Dictionary to map the directory containing the header files.
* lib_dirs = {*dict of dest_dir:src_dir*} : Dictionary to map the directory containing the dynamic libraries to share.
* share_dirs = {*dict of dest_dir:src_dir*} : Dictionary to map the directory containing shared data.

Additional setup.py commands
----------------------------

* *create_namespace* : create_namespace declared in namespace_packagesusage : python setup.py create_namespace.
* *scons* : call scons scripts, usage : python setup.py scons.
* *alea_install* : wrap easy_install command, usage : python setup.py alea_install.
* *alea_upload* : upload distribution forge on the openalea gforge
* *build_sphinx* : launch sphinx on the doc directory

For more information see : 

.. code-block:: python

    python setup.py –help-commands

                                  
Setup.py example
----------------

.. code-block:: python

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

