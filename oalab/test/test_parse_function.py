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
from openalea.oalab.model.parse import has_step, has_animate, has_init, has_run, parse_functions


def test_detect_step_and_others():
    model_src = '''"""
This is the doc of my model
"""

print "result = 0"
result = 0

def step():
    result += 1
    print result

def animate():
    for i in range(10):
        step()

def init():
    result = 0
    print "ini"
'''

    model_src2 = '''"""
This is the doc of my model

:use: run()
"""

print "result = 0"
result = 0

def run():
    for i in range(10):
        result += 1
        print result

'''
    # assert has_step(model_src)
    # assert has_animate(model_src)
    # assert has_init(model_src)
    # assert not has_run(model_src)
    #
    # # assert (True, True, True, False) == parse_functions(model_src)
    #
    # assert not has_step(model_src2)
    # assert not has_animate(model_src2)
    # assert not has_init(model_src2)
    # assert has_run(model_src2)
