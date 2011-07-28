# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


# from PyQt4.QtCore import QObject,SIGNAL
# from PyQt4.QtGui import (QWidget,QLabel,QPixmap,
#                          QHBoxLayout,QVBoxLayout,
#                          QColor,QCursor,QApplication)

# from openalea.core import Node
# from openalea.visualea.node_widget import NodeWidget

# from openalea.spatial_image import palette_names,palette_factory
# from openalea.vtissue.user_registration_gui import UserRegistrationWindow
# from openalea.vtissue.viewer import Viewer
# from openalea.vtissue import reconstruction

# import numpy as np

# #def user_registration(reference_image,floating_image,landmark):
# #    return reference_image,floating_image,landmark


# class UserRegistrationWidget(NodeWidget,UserRegistrationWindow) :
#     """
#     """
#     def __init__ (self, node, parent = None) :

# 	UserRegistrationWindow.__init__(self)
#     	NodeWidget.__init__(self, node)

#         self.landmark = None
# 	self.v1 = Viewer()
#         self.v2 = Viewer()

# 	self.notify(node,("input_modified",0) )

#     def notify(self, sender, event):
#         """Notification sent by node
#         """
#         if event[0] == 'input_modified' :
#             data_ref = self.node.get_input(0)
#             if data_ref is not None :
#                 self.v1.set_image(data_ref)
#                 cmax = data_ref.max()
#                 palette = palette_factory('grayscale',cmax)
#                 self.v1.set_palette(palette)
#                 self.v1._action_open.setChecked(True)
#                 self.v1._action_open.setEnabled(False)
#                 self.set_view(self.v1)

# 	    data_flo = self.node.get_input(1)
# 	    if data_flo is not None :
#                 self.v2.set_image(data_flo)
#                 cmax = data_flo.max()
#                 palette = palette_factory('grayscale',cmax)
#                 self.v2.set_palette(palette)
#                 self.v2._action_open.setChecked(True)
#                 self.v2._action_open.setEnabled(False)
#                 self.set_view(self.v2)

#             pts = self.node.get_input(2)

#             print "pts changed", pts
#             self.node.set_input(3, pts)
#             if pts is not None:
#                 xyzref = pts[:,0:3]
#                 xyzflt = pts[:,3:6]
#                 self.v1.set_points(xyzref)
#                 self.v2.set_points(xyzflt)


# class UserRegistration(Node):
#     """ VisuAlea version of baladin
#     """

#     def __init__(self):
#         Node.__init__(self,

#         inputs = [  {"name" : "reference_image", "interface" : None},
#                     {"name" : "floating_image", "interface" : None},
#                     {"name" : "landmark", "interface" : None},
#                     {"name" : "pts", "interface" : None, "hide" : True}
#                  ],

#         outputs = [ {"name" : "user-linear transformation", "interface" : None}])


#     def __call__(self, inputs):

#         reference_image = self.get_input("reference_image")
#         floating_image = self.get_input("floating_image")

#         pts = self.get_input("pts")
#         matrix_points = np.array(pts)

#         vrx = reference_image.resolution[0]
#         vry = reference_image.resolution[1]
#         vrz = reference_image.resolution[2]

#         vfx = floating_image.resolution[0]
#         vfy = floating_image.resolution[1]
#         vfz = floating_image.resolution[2]

#         T = None
#         if matrix_points.size > 1 :
#             # explain in the voxel world
#             matrix_points[:,0] *= vrx
#             matrix_points[:,1] *= vry
#             matrix_points[:,2] *= vrz
#             matrix_points[:,3] *= vfx
#             matrix_points[:,4] *= vfy
#             matrix_points[:,5] *= vfz

#             x,y = np.hsplit(matrix_points, 2)
#             T = reconstruction.rigid_registration(x,y)

#         return T,
