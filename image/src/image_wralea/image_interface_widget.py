# -*- python -*-
#
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
#
#       File author(s): Chopard
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""Declaration of IImage interface widget
"""

__license__ = "Cecill-C"
__revision__ = " $Id: interface.py 2245 2010-02-08 17:11:34Z cokelaer $"

from openalea.vpltk.qt import QtCore, QtGui
from openalea.core.observer import lock_notify
from openalea.core.interface import IInterfaceWidget,make_metaclass
from image_interface import IImage
from openalea.image.gui.pixmap import to_pix
from openalea.image.gui.pixmap_view import ScalableLabel

class IImageWidget (IInterfaceWidget, QtGui.QMainWindow) :
    """Interface for images expressed as array of triplet of values
    """
    __interface__ = IImage
    __metaclass__ = make_metaclass()

    def __init__(self, node, parent, parameter_str, interface):
        """Constructor

        :Parameters:
            - `node` (Node) - node that own the widget
            - `parent` (QWidget) - parent widget
            - `parameter_str` (str) - the parameter key the widget is associated to
            - `interface` (Ismth) - instance of interface object
        """
        
        QtGui.QMainWindow.__init__(self,parent)
        IInterfaceWidget.__init__(self,node,parent,parameter_str,interface)
        self.setMinimumSize(100,50)

        #ui
        self._lab = ScalableLabel()
        self.setCentralWidget(self._lab)

        self._bot_toolbar = QtGui.QToolBar("slider")

        self._img_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self._img_slider.setEnabled(False)
        QtCore.QObject.connect(self._img_slider,
                        QtCore.SIGNAL("valueChanged(int)"),
                        self.slice_changed)

        self._bot_toolbar.addWidget(self._img_slider)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,self._bot_toolbar)
        self._bot_toolbar.hide()

        #update
        self.notify(node,("input_modified",self.param_str) )

    @lock_notify
    def notify(self, sender, event):
        """Notification sent by node
        """
        if event[0] == "input_modified" :
            self.set_image(self.node.get_input(self.param_str))

    def set_image (self, img) :
        """Change the displayed image
        """
        self._img = img

        if img is None :
            self._lab.setText("no pix")
            self._img_slider.setEnabled(False)
            self._bot_toolbar.hide()
        else :
            if len(img.shape) == 3 :
                self._lab.setPixmap(to_pix(img) )
                self._img_slider.setEnabled(False)
                self._bot_toolbar.hide()
            elif len(img.shape) == 4 :
                ind = min(self._img_slider.value(),img.shape[2] - 1)
                self._img_slider.setRange(0,img.shape[2] - 1)
                self._img_slider.setEnabled(True)
                self.slice_changed(ind)
                self._bot_toolbar.show()
            else :
                msg = "Don't know how to display more than 3D images"
                raise UserWarning(msg)

        self.update()

    def slice_changed (self, ind) :
        self._lab.setPixmap(to_pix(self._img[:,:,ind]) )


