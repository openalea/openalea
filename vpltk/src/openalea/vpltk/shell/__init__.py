
def has_full_ipython():
    """
    Check if User can use IPython shell embeded in OpenAlea.
    
    Check IPython, zmq, pygments
    
    :return: True if user can use IPython shell. Else False.
    """
    # Check Python ZeroMQ
    zmq = has_zmq()
    print("ZMQ: %s"%zmq)
    # Check Pygments
    pgm = has_pygments()
    print("Pygments: %s"%pgm)
    # Check IPython
    ipy = has_ipython()
    print("IPython: %s"%ipy)
	
    return zmq & pgm & ipy

def has_ipython():
    """
    Check if User can use IPython shell embeded in OpenAlea.
    
    Check only IPython without is dependencies(zmq, pygments)
    
    :return: True if user can use IPython. Else False.
    """
    return has_deprecated_ipython() | has_new_ipython()

def has_deprecated_ipython():
    """
    Check if User can has IPython 1.0dev deprecated.
    
    :return: True if user can use IPython. Else False.
    """
    try:
        from IPython.kernel.inprocess.ipkernel import InProcessKernel
        from IPython.frontend.qt.console.rich_ipython_widget import RichIPythonWidget
        from IPython.frontend.qt.inprocess_kernelmanager import QtInProcessKernelManager
        return True
    except ImportError:
        return False
        
def has_new_ipython():
    """
    Check if User can has IPython 1.0dev not deprecated.
    
    :return: True if user can use IPython. Else False.
    """
    try:
        from IPython.kernel.inprocess.ipkernel import InProcessKernel
        from IPython.qt.console.rich_ipython_widget import RichIPythonWidget
        from IPython.qt.inprocess import QtInProcessKernelManager
        return True
    except ImportError:
        return False   
        
def has_zmq():
    """
    Check if User can import Python ZeroMQ
    
    :return: True if user can use Python ZeroMQ. Else False.
    """
    try:
        import zmq
        return True
    except ImportError:
        return False        
    
def has_pygments():
    """
    Check if User can import Pygments
    
    :return: True if user can use Pygments. Else False.
    """
    try:
        import pygments
        return True
    except ImportError:
        return False       
    
def has_pyqt4():
    """
    Check if User can import PyQt4
    
    :return: True if user can use PyQt4. Else False.
    """
    try:
        import PyQt4
        return True
    except ImportError:
        return False  