"""
Signal for actions done by the kernel
"""

from zope.interface import Interface

class Listener(Interface):
    """ A listener is a callable object. """
    def __call__(self, signal):
        """ Call method. """

class Listeners(dict):
    def register( self, listener, signals ):
        for s in signals:
            self.setdefaults(s,[]).append(listener)
    
    def unregister( self, listener ):
    	for signal, l in self.iteritems():
	    if listener in l:
	        l.remove(listener)
	            	         
    def dispatch( self, signal):
	if signal not in self:
	    return
	for l in self[signal]:
	    l(signal)


class Signal(object):
    """
    A signal
    """
    pass
        

