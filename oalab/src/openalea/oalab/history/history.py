from openalea.oalab.gui import qt
from collections import OrderedDict

class History(object):
    """ Manage the dict of objects of the scene """
    def __init__(self):
        # Create the history
        self.obj = qt.QObject()
        self.actionChanged = qt.QAction(self.obj)
        self.hist = OrderedDict()
        self.valueChanged()
        
    def add(self, name="unnamed object", obj="None"):
        # add a new object named 'name' in the history
        name = self._check_if_name_is_unique(name)
        self.hist[name] = obj
        self.valueChanged()
        
    def getHistory(self):
        # return the history (dict)
        return self.hist
        
    def reset(self):
        # clean the history
        self.hist = dict()
        self.valueChanged()
        
    def valueChanged(self):
        # emit Qt Signal when the history change
        self.obj.emit(qt.SIGNAL('HistoryChanged'), self.hist)

    def _check_if_name_is_unique(self, name):
        # Check if a control with the same name 'name' is alreadey register
        # in the control manager.
        # If it is the case, the name is changed ("_1" is append).
        # This is realize until the name becomes unique.
        while name in self.hist:
            try:
                end = name.split("_")[-1]
                l = len(end)
                end = int(end)
                end += 1
                name = name[0:-l] + str(end)
            except:    
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
        