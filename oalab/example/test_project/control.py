from openalea.core.service.control import new_control

from openalea.core.interface import IInt

minterface = IInt(min=1, max=30, step=1)
mcontrol = new_control(u'step',minterface,15)

from openalea.core.interface import IStr

minterface = IStr()
mcontrol = new_control(u'x_label',minterface,u'$x^2$')

minterface = IInt(min=1, max=50, step=1)
mcontrol = new_control(u'nb_step',minterface,10)

minterface = IStr()
mcontrol = new_control(u'y_label',minterface,u'y_label')

minterface = IInt(min=1, max=10, step=1)
mcontrol = new_control(u'a',minterface,2)

minterface = IInt(min=1, max=100, step=10)
mcontrol = new_control(u'b',minterface,20)

