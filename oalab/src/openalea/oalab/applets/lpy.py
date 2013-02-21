from openalea.lpy.gui.computationtask import ComputationTaskManager
from openalea.lpy.gui.lpystudio import LPyWindow

class lpyApplet(object):
    def __init__(self):
        """
        @param parent : parent window
        """
        self.lpywindow = LPyWindow()
        
    def new(self):
        self.lpywindow.newfile()
        
    def open(self, fname=None):
        self.lpywindow.openfile(fname)
        
    def save(self, fname=None):
        self.lpywindow.savefile()

    def run(self):
        self.lpywindow.run()
        
    def controls(self):
        """
        :return: a dict which contain controls widgets
        """
        from openalea.lpy.gui.materialeditor import MaterialPanelWidget
        from openalea.lpy.gui.scalareditor import ScalarEditor
        controls = dict()
        controls["color map"] = MaterialPanelWidget
        controls["scalar editor"] = ScalarEditor
        return controls
        