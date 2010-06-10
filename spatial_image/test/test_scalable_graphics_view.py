from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication,QGraphicsScene,QGraphicsPixmapItem
from openalea.spatial_image import (read_inrimage,grayscale,
                                    view_right,view_face,
                                    PixmapStackView,ScalableGraphicsView)

qapp = QApplication([])

img = read_inrimage("SAM.inr.gz")
view = PixmapStackView(img,grayscale(img.max() ) )
view.set_current_slice(20)

rgt = view_right(img)
view2 = PixmapStackView(rgt,grayscale(rgt.max() ) )
view2.set_current_slice(10)

face = view_face(img)
view3 = PixmapStackView(face,grayscale(face.max() ) )
view3.set_current_slice(140)

sc = QGraphicsScene()

item = QGraphicsPixmapItem(view.pixmap() )
item.setTransformationMode(Qt.SmoothTransformation)
item.scale(*view.resolution() )

sc.addItem(item)

item2 = QGraphicsPixmapItem(view2.pixmap() )
item2.setTransformationMode(Qt.SmoothTransformation)
item2.scale(*view2.resolution() )
w,h = view2.pixmap_real_size()
item2.setPos(-1.1 * w,0)

sc.addItem(item2)

item3 = QGraphicsPixmapItem(view3.pixmap() )
item3.setTransformationMode(Qt.SmoothTransformation)
item3.scale(*view3.resolution() )
w,h = view3.pixmap_real_size()
item3.setPos(0,-1.1 * h)

sc.addItem(item3)

lab = ScalableGraphicsView(sc)
lab.show()

qapp.exec_()
