from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.project.project import ConfigObj
from openalea.core.path import path
from openalea.oalab.gui import resources_rc
from openalea.oalab.project.preview import Preview, pretty_print
from math import sqrt

class PrettyPreview(QtGui.QPushButton):
    def __init__(self, project, size=None, parent=None):
        super(PrettyPreview, self).__init__(parent) 
        wanted_size = 200
        if size:
            wanted_size = size
        margin = 10
        self.setMinimumSize(wanted_size,wanted_size)
        self.setMaximumSize(wanted_size,wanted_size)
        self.project = project
        
        layout = QtGui.QGridLayout()     
        icon_name = ":/images/resources/openalealogo.png"
        if len(project.icon):
            if project.icon[0] is not ":":
                #local icon
                icon_name = path(project.path)/project.name/project.icon
                #else native icon from oalab.gui.resources

        text = pretty_print(project.name) + " v" + pretty_print(project.version)
        
        pixmap = QtGui.QPixmap(icon_name)
        size = pixmap.size()
        label = QtGui.QLabel()
        
        if (size.height()>wanted_size) or (size.width()>wanted_size) :
            # Auto-rescale if image is bigger than (wanted_size x wanted_size)
            label.setScaledContents( True )
        
        size = pixmap.size()
        painter = QtGui.QPainter()
        painter.begin(pixmap)
        painter.drawPixmap(0,0,pixmap)
        painter.drawText(margin,0,size.width(),size.height(),84,text)
        painter.end()
        
        label.setPixmap(pixmap)
        
        layout.addWidget(label,0,0)
        self.setLayout(layout)

def main():
    from openalea.vpltk.project.manager import ProjectManager
    import sys
    app = QtGui.QApplication(sys.argv)
    
    widget = QtGui.QWidget()
    layout = QtGui.QGridLayout()  

    project_manager = ProjectManager()
    project_manager.discover()
    projects = project_manager.projects
    # Auto select number of lines and columns to display
    # Here number of lines <= number of columns
    # <=4 -> 2x2 or 2x1, <=9 -> 3x3 or 3x2, <=16 -> 4x4 or 4x3, ...
    maxcolumn = int(sqrt(len(projects)))+1

    def showDetails():
        sender = QtGui.QPushButton().sender()
        preview_widget = Preview(project=sender.project)
        
        # remove old widget
        item = layout.itemAtPosition(maxcolumn,0)
        if item:
            wid = item.widget()
            layout.removeWidget(wid)
            wid.setParent(None)
            
        layout.addWidget(preview_widget, maxcolumn, 0, maxcolumn, maxcolumn)

    i,j = 0,-1
    for project in projects:
        project.load_manifest()
        # Create widget
        preview_widget = PrettyPreview(project,size=200,parent=widget)
        preview_widget.clicked.connect(showDetails)
        
        if j < maxcolumn-1:
            j += 1
        else:
            j = 0
            i += 1
        layout.addWidget(preview_widget, i, j)

    widget.setLayout(layout)
    # Display
    widget.show()
    app.exec_()

if __name__ == "__main__":
    main()
