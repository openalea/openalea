from openalea.core.node import AbstractNode, Node

try:
    from PyQt4.Qt import QCoreApplication,QApplication,QDialog
    __visual_print_enabled = True
    from ui_vprint import Ui_Dialog
    
    class VisualPrintDialog (QDialog,Ui_Dialog):
        def __init__(self,parent = None):
            if parent:
                QDialog.__init__(self,parent)
            else:
                QDialog.__init__(self)
            Ui_Dialog.__init__(self)
            self.setupUi(self)
            
except:
    print 'visual print disabled'
    __visual_print_enabled = False

    

class VPrint(Node):
    """ Visual Print
    In 0 : The object to display
    In 1 : The caption of the display
    In 2 : The function to transform the object into a string (default=str)
    In 3 : Blocking display

    Out 0 : The object
    """
    def __init__(self,*args):
        Node.__init__(self,*args)
        self.widget = None
        self.enabled = not (QCoreApplication.instance() is None)
    
    def __call__(self, inputs):
        obj = inputs[0]
        caption = inputs[1]
        if caption is None:
            caption = 'Value is'
        blocking = inputs[2]
        if blocking is None:
            blocking = False
        strfunc = inputs[3]
        if strfunc is None:
            strfunc = str
        txt = strfunc(obj)
        if self.enabled:            
            if self.widget is None:
                mw = QApplication.topLevelWidgets()[0]
                self.widget = VisualPrintDialog(parent=mw)
            if self.widget.isModal() != blocking and self.widget.isVisible():
                self.widget.hide()
            self.widget.setModal(blocking)
            self.widget.valueDisplay.setText(txt)
            self.widget.captionText.setText(caption+':')
            if self.widget.isVisible():
                self.widget.activateWindow()
            else:
                if blocking:
                    self.widget.exec_()
                else:
                    self.widget.show()
        else:
            print(caption+':'+txt)
        return (obj,)


