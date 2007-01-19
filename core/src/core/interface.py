# """
# This module contain all the interfaces of the kernel

# :Version: 0.0.1
# :Authors: Szymon Stoma, Christophe Pradal

# """
# import zope.interface as izope
# from zope.interface import Interface, Attribute

# class INode( Interface ):
#     """
#     A Node is a callable object with typed inputs and typed outputs.
#     """
#     def __call__(self,*args, **kwds):
#         """
#         Call method with various arguments.
#         """

#     inputs= Attribute('inputs', 'A dictionary of { argument name : type or class }')
#     outputs= Attribute('outputs', 'A dictionary of { argument name : type or class }')
# """
#         Return a list and a dictionary of classes.

#         >>> n.inputs()= ([int,float], {'toto':Worksapce,'epsilon':float })
# """
    

class Interface:
    pass

class IFileStr(Interface):
    pass

class IFloat(Interface):
    pass


class IStr(Interface):
    pass


class IInt(Interface):
    pass

class IBool(Interface):
    pass