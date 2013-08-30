def dependency_filter(dependency):
    """
    Filter names of dependencies to fix some names conflicts
    """
    if dependency == "pywin32":
        return "pywin"
    elif dependency == "openalea":
        return "openalea_formula"
    elif dependency == "setuptools":
        return "setuptools_formula"
    elif dependency == "readline":
        return "mingw_rt"
    elif dependency == "readline-dev":
        return "mingw"
    elif dependency == "compilers-dev":
        return "mingw"
        
    ##################################
    elif dependency == "sip4-dev":
        return "qt4_dev"
    elif dependency == "pyqt4":
        return ["qt4","pyqglviewer"]
    elif dependency == "pyqt4_dev":
        return "qt4_dev"
    elif dependency == "pyqscintilla":
        return "qt4"    
    ##################################
    
    elif dependency == "boostdev":
        return "boost"
    elif dependency == "boostmath":
        return "boost"
    elif dependency == "boostmath-dev":
        return "boost"
    elif dependency == "boostpython":
        return "boost"
    elif dependency == "boostpython-dev":
        return "boost"    
        
    elif dependency == "ann-dev":
        return "ann"   
    elif dependency == "qhull-dev":
        return "qhull"  
    elif dependency == "cgal-dev":
        return "cgal" 
        
    elif dependency == "nose-dev":
        return "nose"   
    elif dependency == "scons-dev":
        return "scons"        
        
    return dependency