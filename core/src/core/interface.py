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
    

class Interface(object):
    pass

class IFileStr(Interface):
    """ File Path interface """
    pass


class IStr(Interface):
    """ String interface """
    pass


class IFloat(Interface):
    """ Float interface """
    
    def __init__(self, min = -2.**24, max = 2.**24):

        self.min = min
        self.max = max
    


class IInt(Interface):
    """ Int interface """
    
    def __init__(self, min = -2**24, max = 2**24):

        self.min = min
        self.max = max


class IBool(Interface):
    """ Bool interface """
    pass


class IEnumStr(Interface):
    """ String enumeration """

    def __init__(self, enum = []):
        self.enum = enum


class IRGBColor(Interface):
    """ RGB Color """
    pass

class IFunction(Interface):
    """ Function interface """
    pass

class ISequence(Interface):
    """ Sequence interface (list, tuple, ...) """
    pass
