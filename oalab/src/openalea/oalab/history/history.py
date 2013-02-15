from openalea.oalab.gui import qt

class History(object):
    def __init__(self):
        self.obj = qt.QObject()
        self.actionChanged = qt.QAction(self.obj)
        self.hist = dict()
        self.valueChanged()
        
    def add(self, name="unnamed object", obj="None"):
        name = self.check_if_name_is_unique(name)
        self.hist[name] = obj
        self.valueChanged()
        
    def getHistory(self):
        return self.hist
        
    def reset(self):
        self.hist = dict()
        self.valueChanged()
        
    def valueChanged(self):
        self.obj.emit(qt.SIGNAL('HistoryChanged'), self.hist)

    def check_if_name_is_unique(self, name):
        # Check if a control with the same name 'name' is alreadey register
        # in the control manager.
        # If it is the case, the name is changed ("_1" is append).
        # This is realize until the name becomes unique.
        while name in self.hist:
            name += "_1"
        return name  
        
        
def main():
    a = 1
    b = 2
    c = 3
    d = "Viva Virtual Plants Lab!!!"

    h = History()
    h.add("a",a)
    h.add("b",b)
    h.reset()
    h.add("c",c)
    h.add("d",d)
    hist = h.getHistory()
    print "We must have two objects in the history:"
    print "c=3 and d='Viva Virtual Plants Lab!!!'.\n"
    print "Here, we have:"
    for h in hist: print h,  hist[h]
    
if( __name__ == "__main__"):
    main()
        