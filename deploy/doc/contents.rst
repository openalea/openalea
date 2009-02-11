.. _deploy:

.. module:: deploy

OpenAlea Deploy documentation
#############################

Module description
==================

.. sidebar:: Summary

    :Version: |version|
    :Release: |release| 
    :Date: |today|
    :Author: `See AUTHORS.txt <../../AUTHORS.txt>`_
    :Changelog: `See ChangeLog.txt <../../ChangeLog.txt>`_
    
.. topic:: general 

    |deploy| supports the installation of OpenAlea packages via 
    the network and manages their dependencies . It is an 
    extension of Setuptools.

    Additional Features :
     - Discover and manage packages in EGG format
     - Declare shared libraries directory and include directories
     - Call SCons scripts
     - Create namespaces if necessary
     - Support post_install scripts
     - Support 'develop' command
     - OpenAlea GForge upload

    It doesn't include any GUI interface (See OpenAlea.DeployGUI for that).


Deploy documentation
==================== 

.. contents:: Table of Contents
   :depth: 3

.. toctree::
    :maxdepth: 1

    deploy/user_index.rst   
    deploy/reference_index.rst

A `PDF <../latex/deploy.pdf>`_ version of |deploy| documentation is available.

 
    
.. seealso::

   More documentation can be found on the
   `openalea <http://openalea.gforge.inria.fr>`__ wiki.



License
=======

|deploy| is released under a Cecill-C License. See `LICENSE.txt <../../LICENSE.txt>`_    

.. note:: Cecill-C license is a LGPL compatible license.




.. |deploy| replace:: OpenAlea.Deploy
