from PyQt4.QtGui import QApplication,QGraphicsScene
from openalea.spatial_image import (read_inrimage,grayscale,
                                    PixmapStackView,ScalableGraphicsView)

img = read_inrimage("SAM.inr.gz")

qapp = QApplication([])

view = PixmapStackView(img[:100,::],grayscale(img.max() ) )
view.set_current_slice(20)

sc = QGraphicsScene()
sc.addPixmap(view.pixmap() )

lab = ScalableGraphicsView(sc)
lab.show()

qapp.exec_()
