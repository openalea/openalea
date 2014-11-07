
from openalea.lpy import Lsystem, AxialTree


# def adapt_axialtree(axialtree, lsystem):
#     """
#     Adapat an axialtree to be viewable in the world (add a method _repr_geom_)
#
#     :param axialtree: axialtree to adapt
#     :param lsystem: lsystem that can be used to create the 3d representation of axialtree
#     :return: adapted axialtree
#     """
#
#     def repr_geom(self):
#         return __scene
#
#     scene = lsystem.sceneInterpretation(axialtree)
#     axialtree.__scene = scene
#     axialtree._repr_geom_ = types.MethodType(repr_geom, axialtree)
#
#     return axialtree


context = {}

lsystem = Lsystem()
axialtree = AxialTree()
# axialtree = adapt_axialtree(axialtree, lsystem)


code = '''

"""
input = lstring="_(0.01)-(90)F(1)"
output = lstring
"""
N = 2

derivation length: N

production: 

F(x) :
  produce  F(x/3.0)+F(x/3.0)--F(x/3.0)+F(x/3.0)

endlsystem


'''

lsystem.setCode(str(code), context)
lsystem.axiom = "_(0.01)-(90)F(1)"

print('\n----lsystem:')
print(lsystem)
print('\n----axialtree:', axialtree)

axialtree = lsystem.iterate(3)

print('\n----lsystem:')
print(lsystem)
print('\n----axialtree:', axialtree)


lsystem.getLastIterationNb()  # iterate 4 -> getLastIterationNb == 3
lsystem.derivationLength  # see keyword in lpy code

scene = lsystem.sceneInterpretation(axialtree)
print(scene)

world.add(scene, name='test')

# axialtree = adapt_axialtree(axialtree, lsystem)
