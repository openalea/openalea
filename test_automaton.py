# test module
from node import functionfactory

__version__= '0.0.1'
__license__='CECILL'
__institutes__= 'CIRAD'

__doc__="""
This is a test package for creating openalea nodes and 
packages automagically.
"""
__all__= ['plus','moins','viewer']

def plus(a= 0, b= 0):
	return a+b

def moins(a= 0, b= 0):
	return a-b

def viewer():
	from PlantGL import Viewer
	Viewer.start()
	return Viewer

plus= functionfactory(plus,(float,float),(float,))
moins= functionfactory(moins,(float,float),(float,))
viewer= functionfactory(viewer,(),(None,))
