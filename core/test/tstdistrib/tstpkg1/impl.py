
class C1Class1(object):
    pass


class C1Class2(object):
    pass


class C2Class1(object):
    pass


class C2Class2(object):
    pass


class ClassInstatiationError(Exception):
    pass


class C3ClassFailInstantiation(object):

    def __init__(self):
        raise ClassInstatiationError
