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
    a = 1
    b = 2
    c = 3
    d = "Viva Virtual Plants Lab!!!"

    h = History()
    h.append(a)
    h.append(b)
    h.reset()
    h.append(c)
    h.append(d)
    hist = h.getHistory()
    print "We must have two objects in the history:"
    print "c=3 and d='Viva Virtual Plants Lab!!!'."
    print "Here we have:"
    print hist
    
if( __name__ == "__main__"):
    main()
        