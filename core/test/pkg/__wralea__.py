


from openalea.core import *



__editable__ = True
__name__ = "pkg_test"
__version__ = '0.0.1'
__license__= "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = '...'
__url__ = 'http://openalea.gforge.inria.fr'



__all__ = ['file1', 'file2']


file1 = DataFactory(name="file1.txt", editors={'gvim' : 'gvim %s', 'emacs' :'emacs %s'})
file2 = DataFactory(name="file2.txt")
