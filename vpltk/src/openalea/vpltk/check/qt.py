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
	
has_pyqt4()
