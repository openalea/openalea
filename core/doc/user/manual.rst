.. testsetup::

    import openalea.core as core
    import openalea.core.pkgmanager as pkgmanager
    import openalea.math    



Manual
######

.. todo:: complete this manual

.. note:: The following examples assume you have installed the packages and setup your python path correctly. 


Overview
========

.. include:: overview.txt

Installation
============

::

    python setup.py install

Generate this documentation
===========================

::

    python setup.py build_sphinx

                                  
Overview of the different classes
=================================

Create an actor
---------------
The class :class:`IActor<openalea.core.actor.IActor>` implements an interface to emulate a function.

.. doctest::

    >>> import openalea.core as core
    >>> a = openalea.core.actor.IActor()

Create a new package
--------------------
.. doctest:: 

    >>> p = core.Package 

The package manager
-------------------

The module :mod:`openalea.core.pkgmanager` contains a class to manage the packages, which is called :class:`PackageManager<openalea.core.pkgmanager.PackageManager>`. 

.. doctest::
    :options: +SKIP

    >>> pm = pkgmanager.PackageManager()
    >>> pm.init(verbose=False)

The `PackageManager` is a Dictionary of Packages. You can access to its keys using the standard :mod:`dict` methods. If you want to access to a particular `Package`, use the packageManager instance as a dictionary. r instance:

.. doctest::
    :options: +SKIP
    
    >>> pm.keys() 
    >>> pm['openalea.math']

that returns a list of nodes. To access to a particular node, use:

.. doctest::
    :options: +SKIP

    >>> pm['openalea.math']['floor']
    <openalea.core.node.NodeFactory object at 0x936906c>

The `floor` node exists in the `openalea.math` package. The node `floor` is managed through a :class:`NodeFactory<openalea.core.node.NodeFactory>`.



.. topic:: Documentation status

    .. sectionauthor:: Thomas Cokelaer <Thomas Cokelaer __at__ sophia inria fr>
