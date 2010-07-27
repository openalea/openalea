##########################################
# MVC Round trip controlling decorators. #
# Use them in an AOPish way              #
##########################################
class MVCViewStates:
    Undefined          = 0
    FromModelToView    = 1
    FromControlToModel = 2

def MVCView(cls):
    f = cls.__init__ #prevent infinite recursion
    def __wrapinit__(self, *args, **kwargs):
        f(self, *args, **kwargs)
        self.__mvcState = MVCViewStates.Undefined
    cls.__init__ = __wrapinit__
    return cls

def FromModelToView(f):
    def wrap(self, *args, **kwargs):
        self.__mvcState = MVCViewStates.FromModelToView
        f(self, *args, **kwargs)
        self.__mvcState = MVCViewStates.Undefined
    return wrap

def FromControlToModel(f):
    def wrap(self, *args, **kwargs):
        self.__mvcState = MVCViewStates.FromControlToModel
        f(self, *args, **kwargs)
        self.__mvcState = MVCViewStates.Undefined
    return wrap

def onlyOnModelToView(f):
    def wrap(self, *args, **kwargs):
        assert self.__mvcState != MVCViewStates.FromControlToModel
        f(self, *args, **kwargs)
    return wrap

def onlyOnControlToModel(f):
    def wrap(self, *args, **kwargs):
        assert self.__mvcState != MVCViewStates.FromModelToView
        f(self, *args, **kwargs)
    return wrap
