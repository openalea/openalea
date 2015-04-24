"""
Quick Start
===========

Here we suppose that we have a model named *sum_int* that do the sum between two integers. The classical use of this model is:

  - Get the project **(not necessary if you are working inside OpenAleaLab)**:
      >>> from openalea.core.project import ProjectManager
      >>> from openalea.deploy.shared_data import shared_data
      >>> from openalea import oalab
      >>> pm = ProjectManager()
      >>> pm.discover()
      >>> oalab_dir = shared_data(oalab)
      >>> proj = pm.load("sum", oalab_dir)

"""