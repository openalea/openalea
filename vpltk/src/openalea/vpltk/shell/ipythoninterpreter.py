from IPython.inprocess.ipkernel import InProcessKernel

class Interpreter(InProcessKernel):
    """
    Interpreter is an IPython kernel adapt for OpenAlea.
    
    :param gui: GUI to use. Default 'qt4'.
    :param locals: namespace to set to the interpreter. Default 'None'.
    """
    
    def __init__(self, gui="qt4", locals=None):
        super(Interpreter, self).__init__(gui=gui)# cf. get_ipython for ipython singleton problem
        self.locals = self.shell.user_ns
        if locals is not None:
            for l in locals:
                self.locals += l
        self.locals['shell'] = self        

    def runsource(self, source, filename="<input>", symbol="single"):
        """
        Compile code from file, then run it thanks to 'runcode'
        
        :param source: the source string; may contain \n characters
        :param filename: optional filename from which source was read; default "<input>"
        :param symbol: optional grammar start symbol; "single" (default) or "eval"
        :return: True if all is allright, else False.
        
        :warning: "print" problem: sometimes, print is displayed later
        """
        try:
            code = compile(source, filename, symbol)
            if code is not None:
                self.runcode(code)
                return True
            else:
                return False    
        except:
            return False

    def runcode(self, code, store_history=True):
        """
        Run code in IPython Interpreter
        
        :param text: code text to run.
        :return: True if all is allright, else False.
        
        :warning: "print" problem: sometimes, print is displayed later
        """
        try:
            self.shell.run_cell(code, store_history=store_history)
            return True
        except:
            try:
                exec(code)
                return True
            except:
                return False

        
def main():
    from shell import main as main_
    main_()
    
    
if( __name__ == "__main__"):
    main()          