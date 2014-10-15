
class C1Plugin1(object):
    name = 'MyPlugin1'

    def __call__(self):
        from tstpkg1.impl import C1Class1
        return C1Class1


class C1Plugin2(object):
    name = 'MyPlugin2'

    def __call__(self):
        from tstpkg1.impl import C1Class2
        return C1Class2


class C2Plugin1(object):

    def __call__(self):
        from tstpkg1.impl import C2Class1
        return C2Class1


class C2Plugin2(object):

    def __call__(self):
        from tstpkg1.impl import C2Class2
        return C2Class2
