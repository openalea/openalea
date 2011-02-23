# -*- python -*-
#
#       OpenAlea.Secondnature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.secondnature.extendable_objects import Layout

# -- instantiate layouts --
sk = "{0: [1, 2], 1: [5, 6], 2: [3, 4]},"+\
     "{0: None, 1: 0, 2: 0, 3: 2, 4: 2, 5: 1, 6: 1},"+\
     "{0: {'amount': 0.7272727272727273, 'splitDirection': 2}, "+\
     "1: {'amount': 0.16180555555555556, 'splitDirection': 1}, "+\
     "2: {'amount': 0.960352422907489, 'splitDirection': 2},"+\
     "3: {}, 4: {}, 5: {}, 6: {}}"



default = Layout("Default",
                 "Openalea",
                 skeleton = sk,
                 # the widgets we want are those  placed under the
                 # `Visualea` application namespace.
                 # but you could have "PlantGl.viewer" here too.
                 appletmap={3:"Openalea.Interpreter",
                            4:"Openalea.Logger",
                            5:"Openalea.PackageManager"},
                 easy_name="Default Layout")



def get_builtins():
    return [default]
