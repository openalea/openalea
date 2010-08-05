Quick Example
==============

This is a SConstruct file.
See the `scons <http://www.scons.org>`_ documentation for more information.

.. code-block:: python

    import sconsx
    from sconsx import config

    # Creation of a SCons object
    # Set an option file as well as command line args.
    option = Options("options.py", ARGUMENTS)

    # Creation of a SConsX object
    conf = config.Config([ 'install', 'boost.python', 'qt4'])

    # Update the SCons option with the default settings of each tools
    conf.UpdateOptions( options )

    # Creation of the Scons Environment
    env = Environment( options= option )

    # Update the environment with specific flags defined by SConsX and the user.
    conf.Update( env )

    # Generate an help using the command line scons -h
    Help(option.GenerateHelpText(env))

    SConscript(...)


Another equivalent solution is to use the ALEASolution method provided by SConsX:

.. code-block:: python

    import sconsx
    from sconsx import config

    # Creation of a SCons object
    # Set an option file as well as command line args.
    option = Options("options.py", ARGUMENTS)

    env = config.ALEASolution(option, [ 'install', 'boost.python', 'qt4'])
    SConscript(...)


