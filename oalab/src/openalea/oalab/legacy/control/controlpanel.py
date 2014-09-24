from openalea.vpltk.qt import QtGui
from openalea.vpltk.control.abstractcontrolmanager import get_manager


class ControlPanel(QtGui.QTableWidget):
    def __init__(self, row=0, column=1):
        super(ControlPanel, self).__init__(row, column)
        
        headerName = QtGui.QTableWidgetItem("Control")
        self.setHorizontalHeaderItem(0,headerName)
    
    def reset(self):
        self.clear()
        while self.rowCount() > 0:
            self.removeRow( 0 )
        headerName = QtGui.QTableWidgetItem("Control")
        self.setHorizontalHeaderItem(0,headerName)

    def add(self, ctrl):
        row = self.rowCount()
        self.insertRow(row)
        
        manager = get_manager(type(ctrl))
        if manager is not None:
            self.setItem(row,0,manager.displayThumbnail())
        else:
            self.setItem(row,0,QtGui.QTableWidgetItem(str(ctrl)))
        
    def add_several(self, ctrls):
        for ctrl in ctrls:
            self.add(ctrl)
        
    def set(self, ctrl):
        self.reset()
        self.add(ctrl)

    def set_several(self, ctrls):
        self.reset()
        self.add_several(ctrls)

    def new(self):
        pass
        # TODO
        
    def write_all(self):
        ctrls = list()
        for row in self.row():
            for column in self.colunm():
                item = self.item(row, column)
                ctrl = item.writeObject()
                ctrls.append(ctrl)
        return ctrls       
                