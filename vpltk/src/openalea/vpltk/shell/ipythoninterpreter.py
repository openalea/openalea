from IPython.inprocess.ipkernel import InProcessKernel

class Interpreter(InProcessKernel):
    """
    Interpreter is an IPython kernel adapt for OpenAlea.
    
    :param gui: GUI to use. 
    :param locals: namespace to set to the interpreter.
    """
    
    def __init__(self, gui="qt4", locals=None):
        super(Interpreter, self).__init__(gui=gui)
        self.locals = self.shell.user_ns
        if locals is not None:
            for l in locals:
                self.locals += l
        
    def runsource(self, text):
        """
        Run code in IPython Interpreter
        
        :param text: code text to run
        :return: nothing
        """
        self.shell.run_cell(text)
        
    runcode = runsource    
        
        
def main():
    from shell import main as main_
    main_()
    
    
if( __name__ == "__main__"):
    main()          