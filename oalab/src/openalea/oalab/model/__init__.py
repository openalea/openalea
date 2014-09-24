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
  - First, get the model **(the first line is not necessary if you are working inside OpenAleaLab)**:
      >>> Model = proj.get_model
      >>> sum_int = Model("sum_int")
  - Set inputs:
      >>> sum_int.inputs = 1, 2
  - Run model:
      >>> sum_int.run()
      3
      >>> # Or simply:
      >>> sum_int(4, 38)
      42
  - Get result:
      >>> result = sum_int.outputs
      >>> print "4 + 38 = ", result
      4 + 38 =  42

You can get result in the run function:
      >>> result = sum_int.run()
      >>> print result
      42

Usage
=====

Instead of run, you can use other method like *step*, *init*, *animate*:

  - Run only one step of the model:
      >>> model = Model("sum_int")
      >>> result = model.step()
  - Run the model step by step:
      >>> result = model.animate()
  - Set state of the model to initial one:
      >>> result = model.init()

You can set arguments directly inside the brackets. So each following block are equivalents and make a run on a model:

 - Classical:
      >>> model.inputs = 1, 2
      >>> model.run()
      3
 - Shorter:
      >>> model.inputs = 1, 2
      >>> model()
      3
 - Even shorter:
      >>> model.run(1, 2)
      3
 - Shortest
      >>> model(1, 2)
      3
"""