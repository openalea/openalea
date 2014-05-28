from IPython.kernel.inprocess.ipkernel import InProcessKernel


class Interpreter(InProcessKernel):
    """
    Interpreter is an IPython kernel adapted for OpenAlea.
    
    :param gui: GUI to use. Default 'qt4'.
    :param locals: namespace to set to the interpreter. Default 'None'.
    """
    
    def __init__(self, gui="qt4", locals=None):
        super(Interpreter, self).__init__(gui=gui)
        # cf. get_ipython for ipython singleton problem
        self.locals = self.shell.user_ns

        if locals is not None:
            for l in locals:
                self.locals += l  
        self.user_ns = self.shell.user_ns

    def run_cell(self, *args, **kwargs):
        return self.shell.run_cell(*args, **kwargs)

                
def main():
    from shell import main as main_
    main_()
    
    
if( __name__ == "__main__"):
    main()
