from PyQt4.QtGui import QApplication,QPixmap
from openalea.image_wralea.gui.select_box_widget import SelectBoxWidget

class DummyNode (object) :
	def set_input (self, *args) :
		pass

	def get_input(self, *args):
		pass

	def register_listener (self, *args) :
		pass

qapp = QApplication([])

w = SelectBoxWidget(DummyNode() )
w.setPixmap(QPixmap("4_ocean_currents.png") )

w.show()

qapp.exec_()


