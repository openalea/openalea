from PyQt4.QtGui import QApplication,QPixmap
from select_box_widget import SelectBoxWidget

class DummyNode (object) :
	def set_input (self, *args) :
		pass
	
	def register_listener (self, *args) :
		pass

qapp = QApplication([])

w = SelectBoxWidget(DummyNode() )
w.setPixmap(QPixmap("/home/chopard/Bureau/toto.png") )

w.show()

qapp.exec_()


