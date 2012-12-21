from openalea.core import *


__name__ = 'openalea.image.registration.matrix'

__editable__ = True
__description__ = 'Nodes that compute transforms between images and compute resampled images'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr/doc/openalea/pylab/doc/_build/html/contents.html'
__alias__ = []
__version__ = '0.9.0'
__authors__ = 'Daniel BARBEAU'
__institutes__ = 'INRIA/CIRAD'
#__icon__ = 'icon.png'


# -- This is what is used by the package manager to identify what to load --
__all__ = []





################################
# TRANSFORM MATRIX CONVERSIONS #
################################


matrix_real_to_voxels = Factory(name='real2voxels',
                                authors='Eric Moscardi',
                                category='vtissue',
                                nodemodule='matrix',
                                nodeclass='matrix_real2voxels',
                                inputs=({'interface': None, 'name': 'mat', 'desc':"4x4 (homogeneous) real->real matrix"},
                                        {'interface': None, 'name': 'target_base', 'desc':"base for the matrix' target world"},
                                        {'interface': None, 'name': 'source_base', 'desc':"base for the matrix' source world"}),
                                outputs=({'interface': None, 'name': '4x4 source->target matrix'},),
                                widgetmodule=None,
                                widgetclass=None,
                                )

__all__.append("matrix_real_to_voxels")


matrix_voxels_to_real = Factory(name='voxels2real',
                                authors='Eric Moscardi',
                                category='vtissue',
                                nodemodule='matrix',
                                nodeclass='matrix_voxels2real',
                                inputs=({'interface': None, 'name': 'mat', 'desc':"4x4 (homogeneous) source->target matrix"},
                                        {'interface': None, 'name': 'target_base', 'desc':"base for the matrix' target world"},
                                        {'interface': None, 'name': 'source_base', 'desc':"base for the matrix' source world"}),
                                outputs=({'interface': None, 'name': '4x4 real->real matrix'},),
                                widgetmodule=None,
                                widgetclass=None,
                                )

__all__.append("matrix_voxels_to_real")

read_matrix = Factory(name='read_matrix',
                                authors='Daniel Barbeau',
                                category='vtissue',
                                nodemodule='matrix',
                                nodeclass='read_matrix',
                                inputs=({'interface': "IFileStr", 'name': 'file', 'desc':"a file containing a matrix"},),
                                outputs=({'interface': None, 'name': 'The read matrix'},),
                                widgetmodule=None,
                                widgetclass=None,
                                )

__all__.append("read_matrix")


