from openalea.oalab.gui import qt

class History(object):
    def __init__(self):
        self.obj = qt.QObject()
        self.actionChanged = qt.QAction(self.obj)
        self.list = []
        self.valueChanged()
        
    def append(self, a):
        self.list.append(a)
        self.valueChanged()
        
    def getHistory(self):
        return self.list
        
    def reset(self):
        self.list = []
        self.valueChanged()
        
    def valueChanged(self):
        self.obj.emit(qt.SIGNAL('HistoryChanged'), self.list)  
        
        
def main():
    pass

    
if( __name__ == "__main__"):
    main()
        