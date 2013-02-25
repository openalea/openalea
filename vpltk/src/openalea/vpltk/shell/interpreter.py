from IPython.inprocess.ipkernel import InProcessKernel

class Interpreter(InProcessKernel):
    """
    Interpreter is an IPython kernel adapt for OpenAlea.
    """
    
    def __init__(self, gui="qt4", locals=None):
        super(Interpreter, self).__init__(gui="qt4")
        self.locals = self.shell.user_ns
        
    def runsource(self, s):    
        self.shell.run_cell(s)
        
        
def main():
    from shell import main as main_
    main_()
    
    
if( __name__ == "__main__"):
    main()          