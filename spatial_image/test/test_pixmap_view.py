from PyQt4.QtGui import QApplication
from openalea.spatial_image import (read_inrimage,grayscale,
                                    PixmapStackView,ScalableLabel)

img = read_inrimage("SAM.inr.gz")

qapp = QApplication([])

view = PixmapStackView(img[:100,::],grayscale(img.max() ) )

for i in xrange(view.nb_slices() ) :
	print i
	view.set_current_slice(i)
	pix = view.pixmap()
#	pix.save("im%.4d.png" % i)

view.set_current_slice(20)

pix = view.pixmap()
pix.save("0.png")
for i in xrange(1,5) :
	view.rotate(1)
	pix = view.pixmap()
#	pix.save("%d.png" % i)

lab = ScalableLabel()
lab.set_resolution(*img.resolution[:2])
lab.setPixmap(view.pixmap() )
lab.show()

qapp.exec_()
