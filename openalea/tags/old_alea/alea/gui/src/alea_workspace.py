import sys
from PyQt4 import QtCore, QtGui

show_mode = [ True, True ]

MARGIN = 5
CONNECTOR_THICKNESS = 10
CONNECTOR_WIDTH=.75
CONNECTOR_FG_COLOR = QtGui.QColor( 0, 0, 0 )
CONNECTOR_BG_COLOR = QtGui.QColor( 50, 50, 50 )
BOX_FG_COLOR = QtGui.QColor( 0, 0, 0 )
BOX_BG_COLOR = QtGui.QColor( 200, 200, 200 )

SELECTED_LINE_PEN = QtGui.QPen( QtGui.QColor( 255, 0, 0 ) )
LINE_PEN = QtGui.QPen( QtGui.QColor( 0, 0, 0 ) )

class MCanvas( QtGui.QFrame ):
  def __init__(self):
    QtGui.QFrame.__init__( self)
    
  def setX( self, val ):
    localY = self.y()
    self.move(val,localY)
  
  def setY( self, val ):
    localX = self.x()
    self.move(localX,val)
    
  def setSize( self, width, height ):
    self.setFixedSize( width, height )
  
  def show( self,paint):
    self.drawShape(paint)
    

class WSWidget( MCanvas ): #QCanvasRectangle ):
  """
  """
  def __init__( self, icon, widget, painter ):
    #QCanvasRectangle.__init__( self, canvas )
    MCanvas.__init__( self)
    self.icon = icon
    self.widget = widget
    self.main_box = QtCore.QRect( 0,0,0,0 )
    self.input_box = QtCore.QRect( 0,0,0,0 )
    self.output_box = QtCore.QRect( 0,0,0,0 )
    self.param_box = QtCore.QRect( 0,0,0,0 )
    self.inputs = []
    self.params = []
    self.outputs = []

  def collidesWith( self, other ):
    """
    Returns TRUE if the canvas item will collide with the other item after they have moved by their current velocities; otherwise returns FALSE.

    However, we do not care about it, so it always return False.
    """
    return False

  def is_in_mainbox( self, pos ):
    return self.main_box.contains( pos )

  def is_in_inputbox( self, pos ):
    return self.input_box.contains( pos )

  def is_in_outputbox( self, pos ):
    return self.output_box.contains( pos )

  def is_in_parambox( self, pos ):
    return self.param_box.contains( pos )

  def connect_input( self, line ):
    self.inputs.append( line )
    pos1 = line.startPoint()
    pos2 = self.input_box.center()
    line.setPoints( pos1.x(), pos1.y(), pos2.x(), pos2.y() )

  def disconnect_input( self, line ):
    self.inputs.remove( line )

  def connect_output( self, line ):
    self.outputs.append( line )
    pos1 = self.output_box.center()
    pos2 = line.endPoint()
    line.setPoints( pos1.x(), pos1.y(), pos2.x(), pos2.y() )

  def disconnect_output( self, line ):
    self.outputs.remove( line )

  def connect_param( self, line ):
    self.params.append( line )
    pos1 = line.startPoint()
    pos2 = self.param_box.center()
    line.setPoints( pos1.x(), pos1.y(), pos2.x(), pos2.y() )

  def disconnect_param( self, line ):
    self.params.remove( line )

  def drawShape( self,paint):
    """
    Draw the widget in the canvas.

    :Parameters:
      - `paint`: object used to paint

    :Types:
      - `paint`: qt.QPainter
    """

    paint.translate( self.x(),self.y())
    #print "X = %s, Y = %f" % ( self.x(), self.y() )

    box_height = 2*MARGIN
    box_width = MARGIN
    icon_height = 0
    text_height = 0
    text = self.widget
    if show_mode[ 0 ] and self.icon is not None: # If icon is drawn
      box_width += self.icon.width() + MARGIN
      icon_height = self.icon.height()
    if show_mode[ 1 ]: # If text is drawn
      #assert paint.isActive()
      metrics = paint.fontMetrics()
      text_rect = metrics.boundingRect( text )
      #rect = metrics.size( qt.Qt.SingleLine, text )
      text_width = text_rect.width()
      box_width += text_width + MARGIN
      #text_height = text_rect.height()
      text_height = metrics.height()
    if text_height < icon_height:
      box_height += icon_height
    else:
      box_height += text_height
    height = box_height + CONNECTOR_THICKNESS
    width = box_width + 2*CONNECTOR_THICKNESS
    self.setSize( width, height )

    # Draw the main box
    paint.setBrush( BOX_BG_COLOR )
    paint.setPen( BOX_FG_COLOR )
    paint.drawRect( CONNECTOR_THICKNESS, 0, box_width, box_height )

    self.main_box = QtCore.QRect( self.x() + CONNECTOR_THICKNESS, self.y(), box_width, box_height )

    # Draw the connectors
    paint.setBrush( CONNECTOR_BG_COLOR )
    paint.setPen( CONNECTOR_FG_COLOR )
    connector_top = ( 1-CONNECTOR_WIDTH )/2*box_height
    connector_height = CONNECTOR_WIDTH*box_height
    paint.drawRect( 0, connector_top, CONNECTOR_THICKNESS, connector_height )
    self.input_box = QtCore.QRect( self.x(), self.y()+connector_top, CONNECTOR_THICKNESS, connector_height )

    paint.drawRect( box_width+CONNECTOR_THICKNESS, connector_top, CONNECTOR_THICKNESS, connector_height )
    self.output_box = QtCore.QRect( self.x()+box_width+CONNECTOR_THICKNESS, self.y()+connector_top, CONNECTOR_THICKNESS, connector_height )

    connector_left = ( 1-CONNECTOR_WIDTH )/2*box_width+CONNECTOR_THICKNESS
    connector_width = CONNECTOR_WIDTH*box_width
    paint.drawRect( connector_left, box_height, connector_width, CONNECTOR_THICKNESS )
    self.param_box = QtCore.QRect( self.x()+connector_left, self.y()+box_height, connector_width, CONNECTOR_THICKNESS )

    # Draw the icon
    current_left = CONNECTOR_THICKNESS+MARGIN
    mean_height = box_height/2
    if show_mode[ 0 ] and self.icon is not None: # If icon is drawn
      paint.drawPixmap( current_left, mean_height - ( icon_height/2 ), self.icon )
      current_left += self.icon.width() + MARGIN
    if show_mode[ 1 ]: # If text is drawn
      left = current_left
      top = MARGIN+mean_height
      paint.drawText( left, top, text )

    paint.translate( -self.x(), -self.y() )

  def move_by( self, dx, dy ):
    self.moveBy( dx, dy )
    for l in self.inputs:
      st = l.startPoint()
      en = l.endPoint()
      l.setPoints( st.x(), st.y(), en.x()+dx, en.y()+dy )
    for l in self.params:
      st = l.startPoint()
      en = l.endPoint()
      l.setPoints( st.x(), st.y(), en.x()+dx, en.y()+dy )
    for l in self.outputs:
      st = l.startPoint()
      en = l.endPoint()
      l.setPoints( st.x()+dx, st.y()+dy, en.x(), en.y() )

      
MOVE_BOX, MOVE_LINE, SELECTED_LINE = range( 3 )


class WSCanvas(QtGui.QWidget):
    def __init__(self, parent = None,name = ""):
    	self.cnv = QtGui.QFrame()
        QtGui.QWidget.__init__(self, parent)
        self.pen = QtGui.QPen()
        self.brush = QtGui.QBrush()
	self.selected = None
	self.current_line = None
	self.mode = None	
	
	self.object_list = []
	

    def paintEvent(self, event):
        #rect = QtCore.QRect(10, 20, 80, 60)
	#painter.drawRect(rect)
	self.painter = QtGui.QPainter()
        self.painter.begin(self)
        self.painter.setPen(self.pen)
        self.painter.setBrush(self.brush)	
	
	self.loaded_pixmap=QtGui.QPixmap()
	self.loaded_pixmap.load( "loaded.png" )
   	self.ex = WSWidget( self.loaded_pixmap, "Toto pas la", self.painter )
    	self.ex.setX( 50 )
    	self.ex.setY( 80 )
    	self.ex.show(self.painter)
	#self.object_list.append(ex)
    	self.ex1 = WSWidget( self.loaded_pixmap, "Sisi il est la", self.painter )
    	self.ex1.setX( 50 )
    	self.ex1.setY( 140 )
    	self.ex1.show(self.painter)
	#self.object_list.append(ex1)
	
    '''def reset_mode( self ):
      if self.mode == SELECTED_LINE:
        it = self.current_line
        #it.setPen( LINE_PEN )
        #it.setZ( 20 )
        self.mode = None
        #self.cnv.update()
      self.mode = None	
      
    def keyPressEvent( self, event ):
      if self.mode == SELECTED_LINE and event.key() & QtCore.Qt.Key_Delete:
        line = self.current_line
        line.source.disconnect_output( line )
        try:
          line.target.disconnect_input( line )
        except ValueError:
          line.target.disconnect_param( line )
        line.hide()
        #self.cnv.update()
        self.mode = None

    def contentsMousePressEvent( self, event ):
      l = self.canvas().collisions(event.pos())
      self.selected = None
      pos = event.pos()
      if event.button() != QtCore.Qt.LeftButton:
        return
      self.reset_mode()
      for it in l:
        if isinstance( it, WSWidget ):
          if it.is_in_mainbox( pos ):
            self.selected = it
            self.selected.setZ( 10 )
            self.selected_pos = QPoint( event.pos() )
            self.cnv.update()
            self.mode = MOVE_BOX
          elif it.is_in_outputbox( pos ):
            self.current_line = QCanvasLine( self.cnv )
	    self.current_line.setPen( SELECTED_LINE_PEN )
            it.connect_output( self.current_line )
            spos = self.current_line.startPoint()
            self.current_line.setPoints( spos.x(), spos.y(), pos.x(), pos.y() )
            self.current_line.setZ( 20 )
            self.current_line.source = it
            self.current_line.show()
            self.cnv.update()
            self.mode = MOVE_LINE
          break
        elif isinstance( it, QCanvasLine ):
          self.mode = SELECTED_LINE
          self.current_line = it
          it.setPen( SELECTED_LINE_PEN )
          it.setZ( 30 )
          self.cnv.update()
  
    def contentsMouseMoveEvent( self, event ):
      pos = event.pos()
      if self.mode == MOVE_BOX:
        delta_pos = pos - self.selected_pos
        self.selected.move_by( delta_pos.x(), delta_pos.y() )
        self.selected_pos = QPoint( pos )
        self.cnv.update()
      elif self.mode == MOVE_LINE:
        spos = self.current_line.startPoint()
        self.current_line.setPoints( spos.x(), spos.y(), pos.x(), pos.y() )
        self.cnv.update()

    def contentsMouseReleaseEvent( self, event ):
      if self.mode == MOVE_LINE:
        pos = event.pos()
        l = self.canvas().collisions(event.pos())
        connected = False
        for it in l:
          if not isinstance( it, WSWidget ):
            continue
          if it.is_in_inputbox( pos ):
            it.connect_input( self.current_line )
            self.current_line.setPen( LINE_PEN )
            self.current_line.target = it
            connected = True
            break
          elif it.is_in_parambox( pos ):
            it.connect_param( self.current_line )
            self.current_line.setPen( LINE_PEN )
            self.current_line.target = it
            connected = True
            break
        if not connected:
          self.current_line.source.disconnect_output( self.current_line )
          self.current_line.hide()
        self.cnv.update()
        self.mode = None
        self.current_line = None
      elif self.mode == MOVE_BOX:
        self.selected.setZ( 0 )
        self.mode = None
        self.selected = None
'''
           
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = WSCanvas()
    window.show()
    sys.exit(app.exec_())
