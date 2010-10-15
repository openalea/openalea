###############################################################################
# -*- python -*-
#
#       pylab function implementation
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Thomas Cokelaer <Thomas.Cokelaer@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""pylab nodes related to drawings in an axe"""

__license__= "Cecill-C"
__revision__=" $Id$ "

#//////////////////////////////////////////////////////////////////////////////


from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple3, IDict

import pylab
from openalea.core.external import add_docstring
from openalea.pylab import tools
from openalea.pylab.tools import CustomizeAxes





class PyLabBox(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='input')
        self.add_output(name='output')

    def __call__(self, inputs):
        from pylab import box
        box()






class PyLabFancyArrowPatch(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name='arrowstyle', interface=IEnumStr(tools.arrowstyles.keys()), value='simple')
        self.add_input(name='edgecolor', interface=IEnumStr(tools.colors.keys()), value='none')
        self.add_input(name='connectionstyle', interface=IEnumStr(tools.connectionstyles.keys()), value='arc3')
        self.add_input(name='mutation_scale', interface=IFloat, value=1)
        #todo for connection style, connectionstyle="angle,angleA=0,angleB=-90,rad=10"
        #todo for arrowstyle:head_length=0.4,head_width=0.2 tail_width=0.3,shrink_factor=0.5 
        self.add_output(name='output', interface=IDict)

    def __call__(self, inputs):

        kwds = {}
        kwds['arrowstyle'] = self.get_input('arrowstyle')
        kwds['edgecolor'] = self.get_input('edgecolor')
        kwds['connectionstyle'] = self.get_input('connectionstyle')
        kwds['mutation_scale'] = self.get_input('mutation_scale')

        return kwds

class PyLabYAArow(Node):
    # do not call the class but use its args and kwrags for others like BBox
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='width', interface=IFloat(0,100,0.1), value=4)
        #figure, xytip and xybase are not needed
        self.add_input(name='headwidth', interface=IFloat(0,100,0.1), value=12)
        self.add_input(name='frac', interface=IFloat(0,1,0.05), value=0.1)
        self.add_input(name='alpha', interface=IFloat(0,1,0.05), value=1)
        self.add_input(name='color', interface=IEnumStr(tools.colors.keys()), value='blue')
    
        self.add_output(name='output', interface=IDict, value = {})
    """
      animated: [True | False]         
      antialiased or aa: [True | False]  or None for default         
      clip_path: [ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
      contains: a callable function         
      edgecolor or ec: mpl color spec, or None for default, or 'none' for no color         
      facecolor or fc: mpl color spec, or None for default, or 'none' for no color         
      figure: a :class:`matplotlib.figure.Figure` instance         
      fill: [True | False]         
      gid: an id string         
      hatch: [ '/' | '\\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*' ]         
      label: any string         
      linestyle or ls: ['solid' | 'dashed' | 'dashdot' | 'dotted']         
      linewidth or lw: float or None for default         
      lod: [True | False]         
      picker: [None|float|boolean|callable]         
      rasterized: [True | False | None]         
      snap: unknown
      transform: :class:`~matplotlib.transforms.Transform` instance         
      url: a url string         
      visible: [True | False]         
      zorder: any number         
    """

    def __call__(self, inputs):
        kwds = {}
        kwds['width']= self.get_input('width')
        kwds['headwidth']= self.get_input('headwidth')
        kwds['frac']= self.get_input('frac')
        kwds['alpha']= self.get_input('alpha')
        kwds['color']= self.get_input('color')
        return kwds

class PyLabBBox(Node):

    def __init__(self):
        Node.__init__(self)

        self.add_input(name='boxstyle',interface=IEnumStr(tools.boxstyles.keys()), value='round')
        self.add_input(name='fc',interface=IFloat(0,1,0.1), value=0.8)
        self.add_input(name='pad',interface=IFloat(0,1,0.1), value=0.3)
        self.add_output(name='output', interface=IDict)
        #todo: ec
    def __call__(self, inputs):
        #from pylab import bbox
        kwds = {}
        kwds['boxstyle'] = self.get_input('boxstyle') + ',pad='+str(self.get_input('pad'))
        kwds['fc'] = str(self.get_input('fc'))
        return kwds 

class PyLabAnnotate(Node):


    """ should include colornap and colorbar options"""
    def __init__(self):
        
        Node.__init__(self)
        self.add_input(name='text', interface=IStr, value=None)
        self.add_input(name='x target position', interface=IFloat, value=0)
        self.add_input(name='y target position', interface=IFloat, value=0)
        self.add_input(name='x text position', interface=IFloat, value=0)
        self.add_input(name='y text position', interface=IFloat, value=0)
        self.add_input(name='target coords', interface=IEnumStr(tools.xycoords.keys()), value='data')
        self.add_input(name='text coords', interface=IEnumStr(tools.xycoords.keys()), value='data')
        self.add_input(name='arrowprops', interface=IDict, value={'arrowstyle':'->', 'connectionstyle':'arc3', 'rad':.2})
        self.add_input(name='bbox', interface=IDict, value=None)
        self.add_output(name='output')

    """
alpha: float (0.0 transparent through 1.0 opaque)         
      animated: [True | False]         
      axes: an :class:`~matplotlib.axes.Axes` instance         
      backgroundcolor: any matplotlib color         
      clip_box: a :class:`matplotlib.transforms.Bbox` instance         
      clip_on: [True | False]         
      clip_path: [ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
      color: any matplotlib color         
      contains: a callable function         
      family or fontfamily or fontname or name: [ FONTNAME | 'serif' | 'sans-serif' | 'cursive' | 'fantasy' | 'monospace' ]         
      figure: a :class:`matplotlib.figure.Figure` instance         
      fontproperties or font_properties: a :class:`matplotlib.font_manager.FontProperties` instance         
      gid: an id string         
      horizontalalignment or ha: [ 'center' | 'right' | 'left' ]         
      label: any string         
      linespacing: float (multiple of font size)         
      lod: [True | False]         
      multialignment: ['left' | 'right' | 'center' ]         
      picker: [None|float|boolean|callable]         
      position: (x,y)         
      rasterized: [True | False | None]         
      rotation: [ angle in degrees | 'vertical' | 'horizontal' ]         
      rotation_mode: unknown
      size or fontsize: [ size in points | 'xx-small' | 'x-small' | 'small' | 'medium' | 'large' | 'x-large' | 'xx-large' ]         
      snap: unknown
 snap: unknown
      stretch or fontstretch: [ a numeric value in range 0-1000 | 'ultra-condensed' | 'extra-condensed' | 'condensed' | 'semi-condensed' | 'normal' | 'semi-expanded' | 'expanded' | 'extra-expanded' | 'ultra-expanded' ]         
      style or fontstyle: [ 'normal' | 'italic' | 'oblique']         
      text: string or anything printable with '%s' conversion.         
      transform: :class:`~matplotlib.transforms.Transform` instance         
      url: a url string         
      variant or fontvariant: [ 'normal' | 'small-caps' ]         
      verticalalignment or va or ma: [ 'center' | 'top' | 'bottom' | 'baseline' ]         
      visible: [True | False]         
      weight or fontweight: [ a numeric value in range 0-1000 | 'ultralight' | 'light' | 'normal' | 'regular' | 'book' | 'medium' | 'roman' | 'semibold' | 'demibold' | 'demi' | 'bold' | 'heavy' | 'extra bold' | 'black' ]         
      zorder: any number         
    """


    def __call__(self, inputs):
        from pylab import annotate, show
        kwds = {}
        
        s = self.get_input('text')
        xy = [self.get_input('x target position'), self.get_input('y target position')]
        xytext = [self.get_input('x text position'), self.get_input('y text position')]
        xycoords = self.get_input('target coords')
        textcoords = self.get_input('text coords')

        annotate(s, xy, xytext, xycoords=xycoords, textcoords=textcoords, bbox=self.get_input('bbox'), arrowprops=self.get_input('arrowprops'))
        show()
        return None





             

class PyLabAxhline(Node,CustomizeAxes):
    """VisuAlea version of pylab.axhline

    :param *y*: the y position
    :param *xmin*: starting x position
    :param *xmax*: ending x position
    :param *hold*: True by default
    :param *kwargs or Line2D*: connect a Line2D object (optional)

    :returns: pylab.axhline output
    :author: Thomas Cokelaer
    .. todo:: should include colormap and colorbar options

    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)
        
        self.add_input(name='axes')
        self.add_input(name='y', interface=IFloat, value=0.5)
        self.add_input(name='xmin', interface=IFloat, value=0.)
        self.add_input(name='xmax', interface=IFloat, value=1.)
        self.add_input(name='hold', interface=IBool, value=True)
        self.add_input(name='kwargs or line2d', interface=IDict, value={'alpha':1.})
                
        self.add_output(name="axes")
        self.add_output(name="line2d")
        
    def __call__(self, inputs):
        from pylab import axhline, Line2D
      

        kwds = {}        
        y = self.get_input('y')
        xmin = self.get_input('xmin')
        xmax = self.get_input('xmax')
        hold = self.get_input('hold')
        
        axes = self.get_axes()
        
        if type(self.get_input('kwargs or line2d')) == Line2D:
            line2d = self.get_input('kwargs or line2d')
            kwds = line2d.properties()
            for this in ['transform','children','axes','path', 'xdata', 'ydata', 'xydata','transformed_clip_path_and_affine']: 
                del kwds[this]
        else:
            kwds = self.get_input('kwargs or line2d')
        
        for axe in axes: 
            line2d = axhline(y, xmin=xmin, xmax=xmax, hold=hold, **kwds)
            axe.add_line(line2d)
            axe.get_figure().canvas.draw()
            
        return self.get_input('axes'), line2d


         

class PyLabAxvline(Node,CustomizeAxes):
    """VisuAlea version of pylab.axhline

    :param *x*: the x position
    :param *ymin*: starting y position
    :param *ymax*: ending y position
    :param *hold*: True by default
    :param *kwargs or Line2D*: connect a Line2D object (optional)

    :returns: pylab.axhline output
    :author: Thomas Cokelaer
    .. todo:: should include colormap and colorbar options

    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)
        
        self.add_input(name='axes')
        self.add_input(name='x', interface=IFloat, value=0.5)
        self.add_input(name='ymin', interface=IFloat, value=0.)
        self.add_input(name='ymax', interface=IFloat, value=1.)
        self.add_input(name='hold', interface=IBool, value=True)
        self.add_input(name='kwargs or line2d', interface=IDict, value={'alpha':1.})
                
        self.add_output(name="axes")
        self.add_output(name="line2d")
                
    def __call__(self, inputs):
        from pylab import axvline, Line2D
        #cleanup
       
        kwds = {}        
        x = self.get_input('x')
        ymin = self.get_input('ymin')
        ymax = self.get_input('ymax')
        hold = self.get_input('hold')
        
        axes = self.get_axes()
        
        if type(self.get_input('kwargs or line2d')) == Line2D:
            line2d = self.get_input('kwargs or line2d')
            kwds = line2d.properties()
            for this in ['transform','children','axes','path', 'xdata', 'ydata', 'xydata','transformed_clip_path_and_affine']: 
                del kwds[this]
        else:
            kwds = self.get_input('kwargs or line2d')
        
        for axe in axes: 
            print x, ymin, ymax, hold, kwds
            line2d = axvline(x, ymin=ymin, ymax=ymax, hold=hold, **kwds)
            axe.add_line(line2d)
            axe.get_figure().canvas.draw()
            
        return self.get_input('axes'), line2d

class PyLabAxhspan(Node, CustomizeAxes):
    """VisuAlea version of pylab.axvspan

    :param *ymin*: starting y position
    :param *ymax*: ending y position
    :param *xmin*: starting x position
    :param *xmax*: ending x position
    :param *hol*: True by default
    :param *kwargs Patch*: connect a Patch object (optional)

    :returns: pylab.axhspan output
    :author: Thomas Cokelaer

    .. todo:: should include colormap and colorbar options
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)
        
        self.add_input(name='axes')
        
        self.add_input(name='ymin', interface=IFloat, value=0)
        self.add_input(name='ymax', interface=IFloat, value=0.5)
        self.add_input(name='xmin', interface=IFloat, value=0)
        self.add_input(name='xmax', interface=IFloat, value=1)
        self.add_input(name='hold', interface=IBool, value=True)
        self.add_input(name='kwargs (Patch)', interface=IDict, value={})
        self.add_input(name='kwargs or line2d', interface=IDict, value={'alpha':1.})
                
        self.add_output(name="axes")
    def __call__(self, inputs):
        from pylab import axhspan
        print self.get_input('kwargs (Patch)')
        res = axhspan(self.get_input('ymin'), self.get_input('ymax'), xmin=self.get_input('xmin'),
                xmax=self.get_input('xmax'), **self.get_input('kwargs (Patch)'))
        return res

class PyLabAxvspan(Node):
    """VisuAlea version of pylab.axvspan

    :param *xmin*: starting x position
    :param *xmax*: ending x position
    :param *ymin*: starting y position
    :param *ymax*: ending y position
    :param *hol*: True by default
    :param *kwargs Patch*: connect a Patch object (optional)

    :returns: pylab.axvspan output

    :author: Thomas Cokelaer
    .. todo:: should include colormap and colorbar options
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='xmin', interface=IFloat, value=0)
        self.add_input(name='xmax', interface=IFloat, value=0.5)
        self.add_input(name='ymin', interface=IFloat, value=0)
        self.add_input(name='ymax', interface=IFloat, value=1)
        self.add_input(name='hold', interface=IBool, value=True)
        self.add_input(name='kwargs (Patch)', interface=IDict, value={})
        self.add_output(name='output')

    def __call__(self, inputs):
        from pylab import axvspan
        print self.get_input('kwargs (Patch)')
        res = axvspan(self.get_input('xmin'), self.get_input('xmax'), ymin=self.get_input('ymin'),
                ymax=self.get_input('ymax'), **self.get_input('kwargs (Patch)'))
        return res

