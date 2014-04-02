from openalea.vpltk.qt import QtGui, QtCore
from openalea.vpltk.project.project import ConfigObj
from openalea.core.path import path
from openalea.oalab.gui import resources_rc

class Preview(QtGui.QWidget):
    def __init__(self, project, parent=None):
        super(Preview, self).__init__(parent)       
        
        layout = QtGui.QGridLayout()       
        icon_name = ":/images/resources/openalea_icon2.png"
        if len(project.icon):
            if project.icon[0] is not ":":
                #local icon
                icon_name = path(project.path)/project.name/project.icon
                #else native icon from oalab.gui.resources

        i = 1
        for label in ["authors:", "description:", "citation:", "license:", "dependencies:", "path:"]:
            layout.addWidget(QtGui.QLabel(label) ,i,0)
            i += 1
        
        image = QtGui.QImage(icon_name)
        label = QtGui.QLabel()
        label.setPixmap(QtGui.QPixmap(image))
        size = image.size()
        if size.height()>50 or size.width()>50 :
            # Auto-rescale if image is bigger than 50x50
            label.setScaledContents( True )
        label.setMinimumSize(50,50)
        label.setMaximumSize(50,50)
        layout.addWidget(label ,0,0)
        
        layout.addWidget(QtGui.QLabel("<b><FONT SIZE = 40>" + project.name + "<\b>") ,0,1)
        layout.addWidget(QtGui.QLabel(str(project.authors)) ,1,1)
        layout.addWidget(QtGui.QLabel(str(project.description)) ,2,1)
        layout.addWidget(QtGui.QLabel(str(project.citation)) ,3,1)
        layout.addWidget(QtGui.QLabel(str(project.license)) ,4,1)
        layout.addWidget(QtGui.QLabel(str(project.dependencies)) ,5,1)
        layout.addWidget(QtGui.QLabel(str(project.path)) ,6,1)
        
        layout.addWidget(QtGui.QLabel("scripts:") ,8,0)
        layout.addWidget(QtGui.QLabel(str(project.scripts.keys())) ,8,1)

        verticalSpacer = QtGui.QSpacerItem(0,0);
        layout.addItem(verticalSpacer, 9, 0,9,1)
        horizontalSpacer = QtGui.QSpacerItem(0, 0)
        layout.addItem(horizontalSpacer, 0, 2,9,2)
        
        self.setLayout(layout)

def main():
    from openalea.vpltk.project.manager import ProjectManager
    import sys
    app = QtGui.QApplication(sys.argv)
    
    tabwidget = QtGui.QTabWidget()
    
    project_manager = ProjectManager()
    project_manager.discover()

    projects = project_manager.projects
    for project in projects:
        project.load_manifest()
        # Create widget
        preview_widget = Preview(project)
        tabwidget.addTab(preview_widget, project.name)
        
    # Display
    tabwidget.show()
    app.exec_()

if __name__ == "__main__":
    main()
