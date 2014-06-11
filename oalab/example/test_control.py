
from openalea.oalab.service import interface

assert 'IInt' in interface.guess(1)
iclass1 = interface.get_class('IInt')
assert interface.get_class(iclass1) == iclass1

iname0 = 'IInt'
iname1 = interface.get_name(iname0)
iname2 = interface.get_name(iclass1)
iname3 = interface.get_name(iclass1())
assert iname1 == iname0
assert iname2 == iname0
assert iname3 == iname0

interface1 = interface.new(iname1, min=1, max=1)
print interface1
interface2 = interface.new(iclass1, min=1, max=2)
print interface2
interface3 = interface.new(interface2, min=1, max=3)
print interface3
interface4 = interface.new(iname1, 1, min=1, max=5)
print interface4
interface5 = interface.new(value=1, min=1, max=4)
print interface5

print [cls for cls in interface.get_class()]
print [iname for iname in interface.get_name()]


from openalea.oalab.service import control
from openalea.oalab.control.control import Control

print Control('a', value=1,
              constraints=dict(min=1, max=2))
print Control('a', 'IInt',
              constraints=dict(min=3, max=4))
print Control('a', 'IInt',
              constraints=dict(min=5, max=6))

print Control('a', 'IInt')
print Control('a', value=4)



print control.create('a', value=1, constraints=dict(min=1, max=2))
print control.create('a', 'IInt', constraints=dict(min=3, max=4))
print control.create('a', 'IInt', value=6, constraints=dict(min=5, max=6))
print control.create('a', 'IInt')
print control.create('a', value=4)




