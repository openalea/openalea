'''
Created on 29 juin 2010

'''
from pickle import dump,load

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from openalea.spatial_image import PixmapStackView,ScalableGraphicsView, grayscale
from openalea.container.utils import IdSetGenerator
import scipy
import sys
from slide_viewer_ui import Ui_MainWindow

class Seed(QMainWindow):

    def __init__ (self, img) :
	QMainWindow.__init__(self)

        self.seeds = []
        self._seed_ids = []
        self._id_gen = IdSetGenerator()

	self.view = PixmapStackView(img,grayscale(img.max() ) )

        self.sc = QGraphicsScene()

        self.item = QGraphicsPixmapItem(self.view.pixmap() )
        self.item.setTransformationMode(Qt.SmoothTransformation)
        self.item.scale(*self.view.resolution() )
        self.item.setFlag(self.item.ItemIsSelectable,False)
	
	
	#central label
        self.sc.addItem(self.item)
        self.lab = ScalableGraphicsView(self.sc)
	
        #toolbar
        self.tools = self.addToolBar("tools")

        self.toolgroup = QActionGroup(self)

        self.action_add_seed = self.tools.addAction("add_seed")
        self.action_add_seed.setCheckable(True)
        self.toolgroup.addAction(self.action_add_seed)

        self.action_del_seed = self.tools.addAction("del_seed")
        self.action_del_seed.setCheckable(True)
        self.toolgroup.addAction(self.action_del_seed)
        
        self.tools.addSeparator()

        self.save_seed=self.tools.addAction('Save seeds')

        QObject.connect(self.save_seed,SIGNAL("triggered(bool)"),self.save)

        
        self.lab.setMouseTracking(True)

	QObject.connect(self.lab,SIGNAL("mouse_press"),self.mouse_pressed)
      	#QObject.connect(self.lab,SIGNAL("mouse_move"),self.mouse_pressed)
 
        self.setCentralWidget(self.lab)
	self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)

    def debug (self) :
        print "debug"
    
    def mouse_pressed (self, event) :
        sc_coords = self.lab.mapToScene(event.pos() )

        if self.action_add_seed.isChecked() :
            self.add_seed(sc_coords)
        elif self.action_del_seed.isChecked() :
            self.del_seed(sc_coords)
        else :
            pass
       
    def add_seed (self, pos, sid = None) :
        rect = self.item.boundingRect()
        if rect.contains(pos) :
            sid = self._id_gen.get_id(sid)
            col = QColor.fromHsv( (sid * 10) % 360,255,255)
            item = self.sc.addEllipse ( -5, -5, 10, 10, QPen(col),QBrush(col) )
            item.setPos(pos)
            item.setFlag(item.ItemIsSelectable)
            
            self.seeds.append(item)
            self._seed_ids.append(sid)

    def del_seed (self,pos) :
	item = self.sc.itemAt(pos)
        if item in self.seeds :
            self.sc.removeItem(item)
            ind = self.seeds.index(item)
            del self._seed_ids[ind]
            self._id_gen.release_id(ind)
            self.seeds.remove(item)

    def clear (self) :
        del self._seed_ids[:]
        self._id_gen.clear()

        for item in self.seeds :
            self.sc.removeItem(item)
        
        del self.seeds[:]

    def set_seeds (self, seeds) :
        self.clear()
        for x,y,sid in seeds :
            self.add_seed(QPointF(x,y),sid)
    
    def save(self):
        pts = []
        for ind,item in enumerate(self.seeds) :
            print item,self._seed_ids[ind]
            pt = self.item.mapFromScene(item.scenePos() )
            pts.append( (pt.x(),pt.y(),self._seed_ids[ind]) )
        dump(pts,open("point list.txt",'w') )
        print pts
    


app = QApplication(sys.argv)
#file_name = '/Users/moscardi/Work/seminaire2010/tissue_wall.png'
file_name = '/Users/moscardi/Work/seminaire2010/src/seminaire_wralea/realtissue.png'

img = scipy.misc.pilutil.imread(file_name)
img = scipy.array([img[:,:,0]]).transpose()

dt = Seed(img)
dt.show()

try :
    seeds = load(open("point list.txt",'rb') )
    dt.set_seeds(seeds)
except IOError :
    pass

app.exec_()
