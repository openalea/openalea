# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Thomas Cokelaer <cokelaer@gmail.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
##############################################################################
"""This module defines category keywords to be used within wralea files"""

__license__ = "Cecill-C"
__revision__ = " $Id: pkgmanager.py 1433 2008-11-27 08:52:19Z cokelaer $ "


class PackageManagerCategory():
    """
    The PackageManagerCategory is a Dictionary of keywords and categories.

    This category list is used by PackageManager to create the list of
    categories in visualea. To do so, it extracts the category fields
    of each node found in the__wralea__.py file.

    Here below is the list of keywords to be used within the __wralea__ files;
    inside the category field. Each of these keywords (left column) corresponds
    to a label (right column) that will appear in the visualea interface.
    For instance, if "image" is found in the __wralea__ file, then the
    corresponding node will appear in "Image Processing/standard category".

    If you provide a keyword that is not in this list, this keyword will not
    be taken into account. However, a keyword may be appended with a "."
    followed by any keywords that will be considered as a subcategory. For
    instance, a category called scene.myScene will appear in the standard
    main category "Scene Design" and in a sub-category myScene.

    For now there are quite a few keywords that correspond to the same
    category. The goal in the mid-term in to merge them so that there is
    only 1 keyword per category.

    =====================   =======================================
    keywords                Category names in VisuAlea
    =====================   =======================================
    image                   Image Processing.standard
    svg                     Image Processing.svg
    datatype                Python Functionalities.Datatype
    functional              Python Functionalities.functional
    math                    Python Functionalities.math
    python                  Python Functionalities.standard
    data                    Raw Data (txt,geom,png,etc)
    tutorial                Tutorial
    workflow                Workflow
    flow control            Workflow
    system                  System Interaction
    io                      Data I/O
    file                    Data I/O
    test                    Test
    misc                    Miscellaneous
    spatial                 Scene Design.spatial
    scene                   Scene Design
    light                   Scene Design.light
    sky                     Scene Design.sky
    PGL Object Generator    Scene Design.PGL
    demo                    Demo
    composite               Composite
    descriptive             Data Processing.statistics
    stat                    Data Processing.statistics
    statistics              Data Processing.statistics
    regression              Data Processing.regression
    fitting                 Data Processing.fitting
    distribution            Data Processing.distribution
    test                    Data Processing.statistical tests
    string                  Data processing.Data Manipulation...
    codec                   Data processing.Data Manipulation...
    fractal analysis        Scene Design.Fractal Analysis
    plot                    Visualisation
    graphics                Visualisation
    graphic                 Visualisation
    visualization           Visualisation
    visualisation           Visualisation
    web                     Web Services
    unclassified            to Classify
    =====================   =======================================
    """

    def __init__(self):
        """ Constructor """

        # note that keywords here below have small caps except PGL
        # the keywords in the wralea files may have big or small caps though
        self.keywords = {
            'image':        'Image Processing.standard',
            'svg':          'Image Processing.svg',
            'datatype':     'Python Functionalities.Datatype',
            'functional':   'Python Functionalities.functional',
            'math':         'Python Functionalities.math',
            'python':       'Python Functionalities.standard',
            'data':         'Raw Data (txt,geom,png,etc)',
            'tutorial':     'Tutorial',
            'workflow':     'Workflow',
            'flow control': 'Workflow',
            'system':       'System Interaction',
            'io':           'Data I/O',
            'file':         'Data I/O',
            'test':         'Test',
            'misc':         'Miscellaneous',
            'spatial':      'Scene Design.spatial',
            'scene':        'Scene Design',
            'light':        'Scene Design.light',
            'sky':          'Scene Design.sky',
            'PGL Object Generator': 'Scene Design.PGL',
            'demo':         'Demo',
            'composite':    'Composite',
            'descriptive':  'Data Processing.statistics',
            'stat':         'Data Processing.statistics',
            'statistics':   'Data Processing.statistics',
            'regression':   'Data Processing.regression',
            'fitting':      'Data Processing.fitting',
            'distribution': 'Data Processing.distribution',
            'test':         'Data Processing.statistical tests',
            'string': 'Data processing.Data Manipulation and Transformation',
            'codec': 'Data processing.Data Manipulation and Transformation',
            'fractal analysis':'Scene Design.Fractal Analysis',
            'plot':         'Visualisation',
            'graphics':     'Visualisation',
            'graphic':      'Visualisation',
            'visualization': 'Visualisation',
            'visualisation': 'Visualisation',
            'web':          'Web Services',
            'unclassified': 'to Classify'}
            # here, I keep "to Classify with a lower case so that it appears
            # at the end of the category list (all others have a big cap)
