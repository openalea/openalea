# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""
---------------------------------------
Project and Project Manager Quick Start
---------------------------------------

You can work directly on project:

.. code-block:: python

    project1 = Project(name="mynewproj", path="/path/to/proj")

    project1.rename("project", "mynewproj", "hello_project")
    project1.start()
    project1.authors = "OpenAlea Consortium and John Doe"
    project1.description = "Test project concept with numpy"
    project1.long_description = '''This project import numpy.
    Then, it create and display a numpy eye.
    We use it to test concept of Project.'''

    project1.add(category="src", name"hello.py", value="print 'Hello World'")
    project1.description = "This project is used to said hello to everyone"

    project1.add("startup", "begin_numpy.py", "import numpy as np")
    project1.add("src", "eye.py", "print np.eye(2)")
    project1.rename("scripts", "eye.py", "eye_numpy.py")

    project1.save()

Or, you can create or load a *project* thanks to the *project manager*.

.. code-block:: python

    from openalea.vpltk.project.manager import ProjectManager
    # Instanciate ProjectManager
    project_manager = ProjectManager()
    # Discover available projects
    project_manager.discover()
    print project_manager.projects

    # Create project in default directory or in specific one
    p1 = project_manager.create('project1')
    p2 = project_manager.create('project2', '/path/to/project')
    # Load project from default directory or in specific one
    p3 = project_manager.load('project3')
    p4 = project_manager.load('project4', '/path/to/project')

    # Load
    project2 = project_manager.load("numpy_project")
    # Run startup
    project2.start()
    # Run script
    project2.run_script("eye_numpy.py")

To search projects that are not located inside default directories:

.. code-block:: python

    project_manager.find_links.append('path/to/search/projects')
    project_manager.discover()
    print project_manager.projects

"""