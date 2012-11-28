from IPython.inprocess.ipkernel import InProcessKernel

class IPyInterpreter(InProcessKernel):
    """
    IPyInterpreter is an IPython kernel adapt for OpenAlea.
    """
    
    def __init__(self, gui="qt4", locals=None):
        super(IPyInterpreter, self).__init__(gui="qt4")

        if locals is None:
            locals = {"__name__": "__console__", "__doc__": None}
        self.locals = self.shell.user_ns
        
    def runsource(self, s, filename="<input>", symbol="single"):    
        # self.shell.write(s)
        # self.shell.run_code(s)
        self.shell.run_cell(s)
        
    def runsource2(self, s, filename="<input>", symbol="single"):
        self.shell.run_code(s)
        self.shell.write(s)
        # self.shell.run_cell(s)        
# Si 's' est un print, il ne s'affichera pas tout de suite.. Il attendra un "Enter" dans le shell pour s'afficher... 




  