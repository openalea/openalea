from openalea.release import Formula

class pyopengl(Formula):
    license = "BSD-style Open-Source license"
    authors = "Mike C. Fletcher"
    description = "Standard OpenGL bindings for Python"  
    py_dependent   = True
    arch_dependent = True 
    version = "3.0.2"       
    download_url = "http://pypi.python.org/packages/any/P/PyOpenGL/PyOpenGL-"+version+".win32.exe"
    homepage = "http://pyopengl.sourceforge.net/"
    download_name  = "pyopengl.exe"
    DOWNLOAD = COPY_INSTALLER = True 