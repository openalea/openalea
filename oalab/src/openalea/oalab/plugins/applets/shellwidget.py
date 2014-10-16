

class ShellWidget(object):

    name = 'ShellWidget'
    alias = 'Shell'
    icon = 'oxygen_utilities-terminal.png'

    def __call__(self):
        from openalea.oalab.shell.shell import get_shell_class
        return get_shell_class()

    def graft(self, **kwds):
        pass

