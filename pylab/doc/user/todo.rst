
Development
###############
.. topic:: in progress
.. contents::


Implentation Choices
====================

subplot versus axes
--------------------

In pylab, plotting functions put results into an `axes`, which is itself embedded within a figure. 
You may have several axes within a single figure. By default axes occupies most of the figure space. 
Therefore only on axes may be put within a figure. To combine several axes within a figure, you have to 
adjust the axes dimensions. In order to ease the adjustements, pylab provides a routine called `subplot`
that create axes with predefined dimensions. This is especially convenient when tables of axes are required.

In VisuAlea we only use `axes` for the time being since subplot and axes are overwritting themself so as 
to prevent the user to use them together. 

plotting arguments
------------------

Plotting functions have most of their arguments available within VisuAlea. Usually they appear as connectors
in the same order as in pylab documentation.


figure and axes options and decorators
--------------------------------------

All plotting nodes inherits from :class:`Plotting`. Connectors on the right such as xlabel, 
title, legend, colorbar, axes and axis are therefore available. However, they can not be customised. 
If you want to do so you need to connect specialised nodes to the corresponding connector. For instance, if
you are using the :class:`PyLabPlot` node and want to have a xlabel that appears in bold red with 
fontsize 16, then look for the xlabel connector and connect the :class:`PyLabXLabel` node to it. 
Change the :class:`PyLabXLabel` properties accordingly.

.. note:: there are many connectors but all the connectors inherited from :class:`Plotting` always appear 
   in the same order on the right of the node.


Plotting functions available within VisuAlea
=============================================



================================================================= ========================================================
plotting Func   Description
================================================================= ========================================================
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabAcorr`         plot the autocorrelation function
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabBar`           make a bar chart
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabBoxPlot`       make a box and whisker plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabHist`          make a histogram 
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabHexBin`        make a 2D hexagonal binning plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabPlot`          make a line plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabscatter`       make a scatter plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabPolar`         make a polar plot on a PolarAxes
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabPie`           pie charts
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabLogLog`        a log log plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabSubplot`       make a subplot (numrows, numcols, axesnum)
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabContour`       make a contour plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabContourf`      make a filled contour plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabCsd`           make a plot of cross spectral density
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabPsd`           make a plot of power spectral density
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabSpecgram`      a spectrogram plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabSemilogx`      log x axis
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabSemilogy`      log y axis
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabStem`          make a stem plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabPcolor`        make a pseudocolor plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabPcolormesh`    make a pseudocolor plot using a quadrilateral mesh
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabStep`
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabQuiver`        make a direction field (arrows) plot
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabFillBetween`   make filled polygons between two curves
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabFill`          make filled polygons
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabErrorBar`      make an errorbar graph
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabImshow`        plot image data
:class:`~openalea.pylab_nodes_wralea.py_pylab.PyLabAcorr`         plot the autocorrelation function
================================================================= ========================================================


Decorator functions available within VisuAlea
=============================================

=============== ========================================================
text            Description
=============== ========================================================
axes
axis
box             set the axes frame on/off state
clabel          label a contour plot
show            show the figures
figure
legend          make an axes legend
xlabel          add an xlabel to the current axes
ylabel          add a ylabel to the current axes
title           add a title to the current axes
text            add some text at location x,y to the current axes
colorbar        add a colorbar to the current figure
savefig         save the current figure
annotate        annotate something in the figure
axhline         draw a horizontal line across axes
axvline         draw a vertical line across axes
axhspan         draw a horizontal bar across axes
axvspan         draw a vertical bar across axes
xlim            set/get the xlimits
ylim            set/get the ylimits
xticks          set/get the xticks
yticks          set/get the yticks

=============== ========================================================

other nodes
===========

=============== ========================================================
classes
=============== ========================================================
line2D          used by plot functions
fontproperties  used by text functions
=============== ========================================================

=============== ===========================
Patches
=============== ===========================
Circle
Rectangle
Polygon
Ellipse
Wedge
Patch
=============== ===========================

equivalent to numpy
====================

=============== ========================================================
Function         Description
=============== ========================================================
random          calls pylab.random
absolute        calls numpy.absolute
arange
meshgrid
=============== ========================================================

to be added in Visualea
========================

=============== ========================================================
=============== ========================================================
quiverkey       that takes as input the output of quiver node. Add 
                legend with quiver arrow legend.
spy             plot sparsity pattern using markers or image
hlines
twinx
plot_date
=============== ========================================================


TODO or cleanup
===============

=============== ========================================================
Function         Description
=============== ========================================================
arrow           add an arrow to the axes
barbs           a (wind) barb plot
barh            a horizontal bar chart
broken_barh     a set of horizontal bars with gaps
clim            adjust the color limits of the current image
figimage        make a figure image
figtext         add text in figure coords
findobj         recursively find all objects matching some criteria
gca             return the current axes
gcf             return the current figure
gci             get the current image, or None
getp            get a graphics property
hist            make a histogram
ioff            turn interaction mode off
ion             turn interaction mode on
isinteractive   return True if interaction mode is on
imread          load image file into array
imsave          save array as an image file
ishold          return the hold state of the current axes
matshow         display a matrix in a new figure preserving aspect
plot_date       plot dates
plotfile        plot column data from an ASCII tab/space/comma delimited file
rc              control the default params
rgrids          customize the radial grids and labels for polar
setp            set a graphics property
show            show the figures
table           add a table to the plot
thetagrids      customize the radial theta grids and labels for polar
xcorr           plot the autocorrelation function of x and y
=============== ========================================================



=============== =========================================================
Command         Description
=============== =========================================================
figimage        add an image to the figure, w/o resampling
figtext         add text in figure coords
fill_betweenx   make filled polygons between two sets of x-values
gca             return the current axes
gcf             return the current figure
gci             get the current image, or None
getp            get a graphics property
imread          load image file into array
imsave          save array as an image file
matshow         display a matrix in a new figure preserving aspect
plotfile        plot data from a flat file
rc              control the default params
setp            set a graphics property
table           add a table to the axes
=============== =========================================================



pylab functions to be implemented in openalea.numpy or openalea.pylab
======================================================================

pylab.hypergeometric           pylab.nan_to_num               pylab.select    pylab.nbytes 
pylab.add                      pylab.i0                       pylab.ndarray 
pylab.add_docstring            pylab.identity                 pylab.ndenumerate              
pylab.add_newdoc               pylab.ifft                     pylab.ndim                     pylab.setbufsize
pylab.add_newdocs              pylab.diagflat                 pylab.ifft2                    pylab.ndindex                  
pylab.alen                     pylab.diagonal                 pylab.ifftn                    pylab.negative                 pylab.setdiff1d
pylab.all                      pylab.ifftshift                pylab.negative_binomial        pylab.seterr
 pylab.ihfft                    .seterrcall
pylab.ALLOW_THREADS            pylab.digitize                 pylab.iinfo                    pylab.newaxis                  pylab.seterrobj
pylab.alltrue                  pylab.disconnect               pylab.imag                     pylab.newbuffer                pylab.setmember1d
pylab.alterdot                 pylab.disp                     pylab.imread                   pylab.new_figure_manager       pylab.set_numeric_ops
pylab.amap                     pylab.dist                     pylab.imsave                   pylab.NINF                     pylab.setp
pylab.amax                     pylab.distances_along_curve    pylab.noncentral_chisquare     pylab.set_printoptions
pylab.amin                     pylab.dist_point_to_segment    pylab.IndexDateFormatter       pylab.noncentral_f             pylab.set_state
pylab.angle                    pylab.divide                   pylab.index_exp                pylab.nonzero                  pylab.set_string_function
pylab.IndexLocator             pylab.norm                     pylab.setxor1d
pylab.Annotation                                  pylab.indices                  pylab.normal                   pylab.shape
pylab.any                      pylab.double                   pylab.inexact                  pylab.normalize                
pylab.append                   pylab.drange                   pylab.inf                      pylab.Normalize              
pylab.apply_along_axis         pylab.Inf                      pylab.norm_flat               
pylab.apply_over_axes          pylab.Infinity                 pylab.normpdf               
pylab.dsplit                   pylab.info                     pylab.not_equal                pylab.short
pylab.dstack                   pylab.infty   
pylab.nper                     pylab.show_config
pylab.inner                    pylab.npv                      pylab.shuffle
pylab.ediff1d                  pylab.insert                   pylab.NullFormatter            pylab.sign
pylab.eig                      pylab.inside_poly              pylab.NullLocator              pylab.signbit
pylab.eigh                     pylab.num2date                 pylab.signedinteger
pylab.eigvals                  pylab.int0                     pylab.num2epoch                pylab.silent_list
pylab.argmax                   pylab.eigvalsh                 pylab.int16                    pylab.number               
pylab.argmin                   pylab.emath                    pylab.int32                    pylab.NZERO               pylab.sinc
pylab.argsort                                    pylab.obj2sctype               pylab.single
pylab.argwhere                 pylab.empty_like               pylab.int8                    pylab.singlecomplex
pylab.around                   pylab.entropy                  pylab.int_asbuffer             pylab.object0            
pylab.array                    pylab.epoch2num                pylab.intc                     pylab.ogrid                    pylab.size
pylab.array2string             pylab.equal                    pylab.integer                                    pylab.Slider
pylab.array_equal              pylab.ERR_CALL                 pylab.interactive              pylab.ones_like                pylab.slopes
pylab.array_equiv              pylab.ERR_DEFAULT              pylab.interp                                       pylab.solve
pylab.array_repr               pylab.ERR_DEFAULT2             pylab.intersect1d              pylab.over                     pylab.sometrue
pylab.array_split              pylab.ERR_IGNORE               pylab.intersect1d_nu           pylab.PackageLoader            pylab.sort
pylab.array_str                pylab.ERR_LOG                  pylab.intp                     pylab.packbits                 pylab.sort_complex
pylab.arrow                   pylab.pareto                   pylab.source
pylab.Arrow                    pylab.ERR_PRINT                pylab.invert                   pylab.path_length           
pylab.ioff                     
pylab.asanyarray               pylab.errstate                 pylab.ion                      pylab.split
pylab.asarray                  pylab.ERR_WARN                 pylab.ipmt                     pylab.permutation             
pylab.asarray_chkfinite        pylab.exception_to_str         pylab.irefft                   pylab.pi                    
pylab.ascontiguousarray                              pylab.irefft2                
pylab.asfarray                 pylab.expand_dims              pylab.irefftn                  pylab.piecewise              
pylab.asfortranarray           pylab.expm1                    pylab.irfft                    pylab.PINF                     pylab.squeeze
pylab.asmatrix                 pylab.exponential              pylab.irfft2                                        pylab.standard_cauchy
pylab.asscalar                 pylab.exp_safe                 pylab.irfftn                   pylab.pinv                     pylab.standard_exponential
pylab.atleast_1d               pylab.extract                  pylab.irr                      pylab.pkgload                  pylab.standard_gamma
pylab.atleast_2d                    pylab.is_closed_polygon        pylab.place                    pylab.standard_normal
pylab.atleast_3d               pylab.f                        pylab.iscomplex                pylab.plot                     pylab.standard_t
pylab.AutoLocator              pylab.fabs                     pylab.iscomplexobj             pylab.plot_date                pylab.std
 pylab.isfinite                 pylab.plotfile                
b.average                  pylab.fastCopyAndTranspose                     pylab.plotting                 
pylab.fft                      pylab.ishold                   pylab.plt                      pylab.stineman_interp
pylab.fft2                     pylab.isinf                    pylab.pmt                     
pylab.fftfreq                  pylab.isinteractive            pylab.poisson                  
pylab.fftn                     pylab.isnan                    pylab.polar                   
pylab.fftpack                  pylab.isneginf                 pylab.PolarAxes                pylab.string0
pylab.fftpack_lite             pylab.is_numlike               pylab.poly                     pylab.strpdate2num
pylab.fftshift                 pylab.isposinf                 pylab.poly1d                   pylab.SU
pylab.bar                      pylab.fftsurr                  pylab.ispower2                 pylab.polyadd                  pylab.subplot
pylab.barbs                    pylab.figaspect                pylab.isreal                   pylab.poly_below               pylab.subplots_adjust
pylab.barh                     pylab.figimage                 pylab.isrealobj                pylab.poly_between             pylab.subplot_tool
pylab.isscalar                 pylab.polyder                  pylab.SubplotTool
pylab.base_repr                pylab.fignum_exists            pylab.issctype                 pylab.polydiv                  pylab.subtract
pylab.bench                    pylab.figtext                  pylab.is_string_like           pylab.polyfit                  pylab.sum
pylab.beta                  
pylab.binary_repr           pylab.issubdtype               pylab.polyint                  pylab.suptitle
pylab.bincount                 pylab.FigureCanvasBase         pylab.issubsctype              pylab.polymul                  pylab.svd
pylab.binomial                  pylab.isvector                 pylab.polysub                  pylab.swapaxes
pylab.bitwise_and                  pylab.iterable                 pylab.polyval                  pylab.switch_backend
pylab.bitwise_not              pylab.power                    pylab.sys
pylab.bitwise_or               pylab.fill_betweenx                                 pylab.ppmt                     pylab.table
pylab.bitwise_xor              pylab.find                     pylab.prctile                  pylab.take
pylab.bivariate_normal         pylab.find_common_type         pylab.kron                     pylab.prctile_rank          
pylab.findobj                  pylab.l1norm                   pylab.prepca                  
pylab.bmat                     pylab.finfo                    pylab.l2norm                                       pylab.tensordot
pylab.bone                     pylab.fix                      pylab.lapack_lite              pylab.prod                     pylab.tensorinv
     pylab.FixedFormatter           pylab.laplace                  pylab.product                  pylab.tensorsolve
pylab.bool8                    pylab.FixedLocator             pylab.ldexp                    pylab.test
pylab.flag                     pylab.left_shift               pylab.ptp                      pylab.Tester
pylab.flatiter                 pylab.legend                   pylab.put                      pylab.text
pylab.broadcast                pylab.flatnonzero              pylab.less                                       pylab.Text
pylab.broadcast_arrays         pylab.flatten                  pylab.less_equal               pylab.pv                       pylab.TH
pylab.broken_barh              pylab.flexible                 pylab.levypdf                  pylab.pylab_setup              pylab.thetagrids
            pylab.fliplr                   pylab.lexsort                  pylab.PZERO                    pylab.TickHelper
    pylab.flipud                   pylab.liaupunov                pylab.qr                       pylab.tile
pylab.Button                     pylab.linalg                 
pylab.LinAlgError                             pylab.trace
pylab.transpose
pylab.LinearLocator            pylab.radians                  pylab.trapz

pylab.can_cast                 pylab.FLOATING_POINT_SUPPORT   pylab.little_endian            pylab.rand                     pylab.triangular
pylab.cast                     pylab.floor                    pylab.load                     pylab.randint                
pylab.cbook                    pylab.floor_divide             pylab.loads                    pylab.trim_zeros
pylab.cdouble                  pylab.fmod                     pylab.loadtxt               
pylab.format_parser            pylab.Locator                  pylab.random_integers          
pylab.center_matrix            pylab.FormatStrFormatter                             pylab.random_sample            pylab.true_divide
pylab.cfloat                   pylab.Formatter                                    pylab.ranf                     pylab.TU
pylab.char                     pylab.FPE_DIVIDEBYZERO         pylab.log1p                    pylab.rank                     pylab.twinx
pylab.character                pylab.FPE_INVALID              pylab.log2                     pylab.RankWarning              pylab.twiny
pylab.chararray                pylab.FPE_OVERFLOW             pylab.LogFormatter             pylab.rate                     pylab.typecodes
pylab.chisquare                pylab.FPE_UNDERFLOW            pylab.LogFormatterExponent     pylab.ravel                    pylab.typeDict
pylab.cholesky                 pylab.FR                       pylab.LogFormatterMathtext     pylab.rayleigh                 pylab.typeNA
pylab.choose                   pylab.frange                   pylab.logical_and              pylab.rc                       pylab.typename
pylab.frexp                    pylab.logical_not              pylab.rcdefaults               pylab.ubyte
pylab.frombuffer               pylab.logical_or               pylab.rcParams                 pylab.ufunc
pylab.fromfile                 pylab.logical_xor              pylab.rcParamsDefault          pylab.UFUNC_BUFSIZE_DEFAULT
pylab.fromfunction             pylab.logistic                 pylab.real                     pylab.UFUNC_PYVALS_NAME
pylab.fromiter                 pylab.LogLocator               pylab.real_if_close            pylab.uint
pylab.clim                     pylab.frompyfunc               pylab.rec                      pylab.uint0
pylab.clip                     pylab.fromregex                pylab.lognormal                pylab.rec2csv                  pylab.uint16
pylab.CLIP                     pylab.fromstring               pylab.logseries                pylab.rec_append_fields        pylab.uint32
pylab.clongdouble              pylab.FuncFormatter                         pylab.recarray                 pylab.uint64
pylab.clongfloat               pylab.fv                       pylab.longcomplex              pylab.rec_drop_fields          pylab.uint8
pylab.gamma                    pylab.longdouble               pylab.reciprocal               pylab.uintc
pylab.gca                      pylab.longest_contiguous_ones  pylab.rec_join                 pylab.uintp
pylab.cohere                   pylab.gcf                      pylab.longest_ones             pylab.record                   pylab.ulonglong
pylab.gci                      pylab.longfloat   
pylab.colormaps                pylab.generic                  pylab.longlong                
pylab.colors                   pylab.geometric                pylab.lookfor                   pylab.uniform
pylab.column_stack             pylab.get                      pylab.lstsq                    pylab.refft                    pylab.union1d
pylab.common_type              pylab.get_array_wrap           pylab.ma                       pylab.refft2                   pylab.unique
pylab.compare_chararrays       pylab.MachAr                   pylab.refftn                   pylab.unique1d
 pylab.get_backend              pylab.mat                      pylab.register_cmap            pylab.unpackbits
pylab.getbuffer                pylab.math                     pylab.relativedelta            pylab.unravel_index
pylab.getbufsize               pylab.matplotlib               pylab.remainder                pylab.unsignedinteger
pylab.matrix                   pylab.repeat                   pylab.unwrap
pylab.complexfloating          pylab.get_current_fig_manager  pylab.matrix_power               pylab.ushort
pylab.compress                 pylab.geterr                   pylab.matshow                  pylab.require                  
pylab.concatenate              pylab.geterrcall               pylab.MAXDIMS                  pylab.reshape                  pylab.var
pylab.cond                     pylab.geterrobj                pylab.maximum                  pylab.resize                   pylab.vdot
pylab.conj                     pylab.get_fignums              pylab.maximum_sctype           pylab.restoredot               pylab.vectorize
pylab.conjugate                pylab.get_include              pylab.MaxNLocator              pylab.rfft                     pylab.vector_lengths
pylab.connect                  pylab.get_numarray_include     pylab.may_share_memory         pylab.rfft2                    pylab.vlines
pylab.get_numpy_include        pylab.mean                     pylab.rfftn                    pylab.void
pylab.getp                     pylab.median                   pylab.rgrids                   pylab.void0
pylab.convolve                 pylab.get_plot_commands        pylab.memmap                   pylab.right_shift              pylab.vonmises
pylab.get_printoptions                        pylab.vsplit
pylab.get_scale_docs           pylab.mgrid                    pylab.rk4                      pylab.vstack
pylab.copy                     pylab.get_scale_names          pylab.minimum                  pylab.rms_flat                 pylab.waitforbuttonpress
pylab.corrcoef                 pylab.get_sparse_matrix        pylab.minorticks_off           pylab.roll                     pylab.wald
pylab.correlate                pylab.get_state                pylab.minorticks_on            pylab.rollaxis                 pylab.warnings
pylab.get_xyz_where            pylab.mintypecode              pylab.roots                    pylab.WE
                pylab.ginput                   pylab.MinuteLocator            pylab.rot90                    pylab.WeekdayLocator
pylab.cov                      pylab.gradient                 pylab.MINUTELY                              pylab.WEEKLY
   pylab.gray                     pylab.mirr                     pylab.row_stack                pylab.weibull
ylab.greater                  pylab.mlab                     pylab.rrule                    pylab.where
pylab.csingle                  pylab.greater_equal            pylab.MO                       pylab.RRuleLocator             pylab.who
pylab.csv2rec                                      pylab.mod                                    pylab.Widget
pylab.ctypeslib                pylab.griddata                 pylab.modf                     pylab.SA                      
                pylab.gumbel                   pylab.MonthLocator             pylab.safe_eval             
pylab.cumproduct               pylab.MONTHLY                  pylab.sample                   pylab.winter
                     pylab.movavg                   pylab.save                     pylab.WRAP
pylab.DAILY                      pylab.mpl                      pylab.xcorr
pylab.DataSource               pylab.helper                   pylab.msort                    pylab.savetxt                  pylab.xlabel
pylab.date2num                 pylab.hexbin                   pylab.multinomial              pylab.savez                   
pylab.DateFormatter            pylab.hfft                     pylab.MultipleLocator          pylab.ScalarFormatter          pylab.xscale
pylab.DateLocator              pylab.hist                     pylab.multiply                 pylab.ScalarType               
pylab.datestr2num              pylab.histogram                pylab.multivariate_normal      pylab.scatter                  pylab.YearLocator
pylab.DayLocator               pylab.histogram2d              pylab.mx2num                   pylab.sci                      pylab.YEARLY
pylab.dedent                   pylab.histogramdd              ylab.sctype2char              pylab.ylabel
pylab.degrees                  pylab.hlines                   pylab.nan                      pylab.sctypeDict
pylab.NaN                      pylab.sctypeNA                 pylab.yscale
pylab.NAN                      pylab.sctypes                  pylab.yticks
pylab.delete                   pylab.HourLocator              pylab.nanargmax                pylab.searchsorted             pylab.zeros
pylab.demean                   pylab.HOURLY                   pylab.nanargmin                pylab.SecondLocator            pylab.zeros_like
pylab.deprecate                pylab.hsplit                   pylab.nanmax                   pylab.SECONDLY                 pylab.zipf
pylab.deprecate_with_doc       pylab.hstack                   pylab.nanmin                   pylab.seed                     
pylab.det                      pylab.hsv                      pylab.nansum                   pylab.segments_intersec


pylab.matplotlib.afm 
pylab.matplotlib.artist                  pylab.matplotlib.matplotlib_fname        
pylab.matplotlib.minor1                 
pylab.matplotlib.minor2                
pylab.matplotlib.backend_bases           pylab.matplotlib.finance                 pylab.matplotlib.s
pylab.matplotlib.backends                pylab.matplotlib.fontconfig_pattern      pylab.matplotlib.mpl                     pylab.matplotlib.scale
pylab.matplotlib.bezier                  pylab.matplotlib.font_manager            
pylab.matplotlib.blocking_input          pylab.matplotlib.ft2font                 pylab.matplotlib.shutil
pylab.matplotlib.generators             pylab.matplotlib.spines
pylab.matplotlib.cbook                   pylab.matplotlib.nn                  
pylab.matplotlib.checkdep_dvipng         pylab.matplotlib.get_backend           
pylab.matplotlib.checkdep_ghostscript    pylab.matplotlib.nxutils                 
pylab.matplotlib.checkdep_pdftops        pylab.matplotlib.get_configdir           pylab.matplotlib.offsetbox               pylab.matplotlib.table
pylab.matplotlib.checkdep_ps_distiller                    pylab.matplotlib.tempfile
pylab.matplotlib.checkdep_tex            pylab.matplotlib.get_data_path           pylab.matplotlib.patches                 pylab.matplotlib.text
pylab.matplotlib.checkdep_usetex         pylab.matplotlib.path                    pylab.matplotlib.ticker
pylab.matplotlib.get_example_data        pylab.matplotlib.tight_bbox

pylab.matplotlib.get_home                pylab.matplotlib.tmp
pylab.matplotlib.get_py2exe_datafiles    pylab.matplotlib.projections             pylab.matplotlib.transforms
pylab.matplotlib.collections             pylab.matplotlib.pylab                   pylab.matplotlib.units
pylab.matplotlib.use
pylab.matplotlib.image                   pylab.matplotlib.pyparsing              
pylab.matplotlib.compare_versions        pylab.matplotlib.pyplot                  pylab.matplotlib.validate_backend
pylab.matplotlib.validate_cairo_format
pylab.matplotlib.converter               pylab.matplotlib.interactive            ylab.matplotlib.validate_toolbar

pylab.matplotlib.dates                   pylab.matplotlib.is_string_like          pylab.matplotlib.rcdefaults             
pylab.matplotlib.key                     pylab.matplotlib.rcParams             
pylab.matplotlib.widgets
pylab.matplotlib.lines                   pylab.matplotlib.rcParamsDefault         
pylab.matplotlib.major                   pylab.matplotlib.rcsetup                 
pylab.matplotlib.mathtext                pylab.matplotlib.re         


pylab.matplotlib.mlab.amap                              pylab.matplotlib.mlab.FormatDate                        pylab.matplotlib.mlab.np
pylab.matplotlib.mlab.base_repr                         pylab.matplotlib.mlab.FormatDatetime                    pylab.matplotlib.mlab.nxutils
pylab.matplotlib.mlab.binary_repr                       pylab.matplotlib.mlab.FormatFloat                       pylab.matplotlib.mlab.operator
pylab.matplotlib.mlab.bivariate_normal                  pylab.matplotlib.mlab.FormatFormatStr                   pylab.matplotlib.mlab.os
pylab.matplotlib.mlab.FormatInt                         pylab.matplotlib.mlab.path_length
pylab.matplotlib.mlab.cbook                             pylab.matplotlib.mlab.FormatMillions                    pylab.matplotlib.mlab.poly_below
pylab.matplotlib.mlab.center_matrix                     pylab.matplotlib.mlab.FormatObj                         pylab.matplotlib.mlab.poly_between
pylab.matplotlib.mlab.FormatPercent                     pylab.matplotlib.mlab.prctile
 pylab.matplotlib.mlab.FormatString                      pylab.matplotlib.mlab.prctile_rank
pylab.matplotlib.mlab.cohere_pairs                      pylab.matplotlib.mlab.FormatThousands                   pylab.matplotlib.mlab.prepca
pylab.matplotlib.mlab.frange 
pylab.matplotlib.mlab.contiguous_regions                pylab.matplotlib.mlab.quad2cubic
pylab.matplotlib.mlab.copy                              pylab.matplotlib.mlab.get_formatd                       pylab.matplotlib.mlab.rec2csv
pylab.matplotlib.mlab.cross_from_above                  pylab.matplotlib.mlab.get_sparse_matrix                 pylab.matplotlib.mlab.rec2txt
pylab.matplotlib.mlab.cross_from_below                  pylab.matplotlib.mlab.get_xyz_where                     pylab.matplotlib.mlab.rec_append_fields
pylab.matplotlib.mlab.griddata                          .matplotlib.mlab.rec_drop_fields
pylab.matplotlib.mlab.csv                               pylab.matplotlib.mlab.rec_groupby
pylab.matplotlib.mlab.csv2rec                           pylab.matplotlib.mlab.identity                          pylab.matplotlib.mlab.rec_join
pylab.matplotlib.mlab.csvformat_factory                 pylab.matplotlib.mlab.rec_keep_fields
pylab.matplotlib.mlab.defaultformatd                    pylab.matplotlib.mlab.inside_poly                       pylab.matplotlib.mlab.rec_summarize
pylab.matplotlib.mlab.is_closed_polygon                
pylab.matplotlib.mlab.demean                            pylab.matplotlib.mlab.ispower2                        
pylab.matplotlib.mlab.kwdocd                            pylab.matplotlib.mlab.rk4
pylab.matplotlib.mlab.l1norm                            pylab.matplotlib.mlab.rms_flat
pylab.matplotlib.mlab.l2norm                            pylab.matplotlib.mlab.safe_isinf
pylab.matplotlib.mlab.less_simple_linear_interpolation  pylab.matplotlib.mlab.safe_isnan
pylab.matplotlib.mlab.dist                              pylab.matplotlib.mlab.levypdf                           pylab.matplotlib.mlab.save
pylab.matplotlib.mlab.distances_along_curve             pylab.matplotlib.mlab.liaupunov                         pylab.matplotlib.mlab.segments_intersect
pylab.matplotlib.mlab.dist_point_to_segment             pylab.matplotlib.mlab.load                              
pylab.matplotlib.mlab.division                          pylab.matplotlib.mlab.log2                              pylab.matplotlib.mlab.slopes
pylab.matplotlib.mlab.entropy                           pylab.matplotlib.mlab.longest_ones                      pylab.matplotlib.mlab.stineman_interp
pylab.matplotlib.mlab.exp_safe                          pylab.matplotlib.mlab.ma                                
pylab.matplotlib.mlab.exp_safe_MAX                      pylab.matplotlib.mlab.math                              pylab.matplotlib.mlab.vector_lengths
pylab.matplotlib.mlab.exp_safe_MIN                      pylab.matplotlib.mlab.movavg                            pylab.matplotlib.mlab.verbose
pylab.matplotlib.mlab.fftsurr                           pylab.matplotlib.mlab.warnings
pylab.matplotlib.mlab.FIFOBuffer                        
pylab.matplotlib.mlab.find                              pylab.matplotlib.mlab.norm_flat                         
pylab.matplotlib.mlab.FormatBool                        pylab.matplotlib.mlab.normpdf   


matplotlib.afm                     matplotlib.dates                   
matplotlib.artist                  matplotlib.default                 matplotlib._havedate               matplotlib.patches                 matplotlib.shutil
matplotlib.image                   matplotlib.path                    matplotlib.spines
matplotlib.backend_bases         
matplotlib.backends          
matplotlib.bezier                   matplotlib.projections             matplotlib.table
matplotlib.blocking_input          matplotlib.is_string_like          matplotlib.pylab                   matplotlib.tempfile
matplotlib.text
matplotlib.cbook                   matplotlib.key                     matplotlib.pyparsing               matplotlib.ticker
matplotlib.checkdep_dvipng               matplotlib.tight_bbox
matplotlib.checkdep_ghostscript    matplotlib.finance                 matplotlib.lines                   
matplotlib.checkdep_pdftops        matplotlib.fontconfig_pattern      matplotlib.major                 
matplotlib.checkdep_ps_distiller   matplotlib.font_manager            matplotlib.mathtext                 matplotlib.transforms
matplotlib.checkdep_tex            matplotlib.ft2font                 matplotlib.rcdefaults              matplotlib.units
matplotlib.checkdep_usetex         matplotlib.generators              matplotlib.matplotlib_fname        
matplotlib.minor1                  matplotlib.rcParams 
matplotlib.minor2                  matplotlib.RcParams                matplotlib.validate_backend
matplotlib.mlab                    matplotlib.rcParamsDefault         matplotlib.validate_cairo_format
matplotlib.get_configdir           matplotlib.mpl                     matplotlib.rcsetup                 matplotlib.validate_toolbar
matplotlib.collections           matplotlib.re 
matplotlib.get_data_path 
matplotlib.compare_versions     matplotlib.get_example_data        matplotlib.nn
 matplotlib.widgets
matplotlib.get_home                matplotlib.nxutils                 matplotlib.s                       
matplotlib.get_py2exe_datafiles    matplotlib.offsetbox               matplotlib.scale                


cumsum    - the cumulative sum along a dimension
----------------------------------------------------
      eig       - the eigenvalues and eigen vectors of v
      find      - return the indices where a condition is nonzero
      fliplr    - flip the rows of a matrix up/down
      flipud    - flip the columns of a matrix left/right
      rand      - an array from the uniform distribution [0,1]
      rot90     - rotate matrix k*90 degress counterclockwise
      squeeze   - squeeze an array removing any dimensions of length 1
      svd       - singular value decomposition
      zeros     - a matrix of zeros

Probability
-----------------
    
      levypdf   - The levy probability density function from the char. func.
      normpdf   - The Gaussian probability density function
      rand      - random numbers from the uniform distribution
    
Statistics
------------------
    
      amax       - the maximum along dimension m
      amin       - the minimum along dimension m
      corrcoef  - correlation coefficient
      cov       - covariance matrix
      mean      - the mean along dimension m
      median    - the median along dimension m
      norm      - the norm of vector x
      prod      - the product along dimension m
      ptp       - the max-min along dimension m
      std       - the standard deviation along dimension m
      asum       - the sum along dimension m
    


Time series analysis
-------------------------
    
      fft       - the fast Fourier transform of vector x
      hist      - compute the histogram of x
      sinc      - the sinc function of array x
    
Dates
-------------
    
      date2num  - convert python datetimes to numeric representation
      drange    - create an array of numbers for date plots
      num2date  - convert numeric type (float days since 0001) to datetime
    
Other
-----------
    
      angle     - the angle of a complex array
      griddata  - interpolate irregularly distributed data to a regular grid

Other
------------
    
      angle     - the angle of a complex array
      griddata  - interpolate irregularly distributed data to a regular grid
      load      - Deprecated--please use loadtxt.
      loadtxt   - load ASCII data into array.
      polyfit   - fit x, y to an n-th order polynomial
      polyval   - evaluate an n-th order polynomial
      roots     - the roots of the polynomial coefficients in p
      save      - Deprecated--please use savetxt.
      savetxt   - save an array to an ASCII file.
      trapz     - trapezoidal integration

patches
--------

* pylab.matplotlib.patches.allow_rasterization
* pylab.matplotlib.patches.Arc
* pylab.matplotlib.patches.Arrow
* pylab.matplotlib.patches.ArrowStyle
* pylab.matplotlib.patches.artist
* pylab.matplotlib.patches.bbox_artist
* pylab.matplotlib.patches.BoxStyle
* pylab.matplotlib.patches.CirclePolygon
* pylab.matplotlib.patches.colors
* pylab.matplotlib.patches.concatenate_paths
* pylab.matplotlib.patches.ConnectionPatch
* pylab.matplotlib.patches.ConnectionStyle
* pylab.matplotlib.patches.division
* pylab.matplotlib.patches.draw_bbox
* pylab.matplotlib.patches.FancyArrow
* pylab.matplotlib.patches.FancyBboxPatch
* pylab.matplotlib.patches.get_cos_sin
* pylab.matplotlib.patches.get_intersection
* pylab.matplotlib.patches.get_parallels
* pylab.matplotlib.patches.inside_circle
* pylab.matplotlib.patches.k
* pylab.matplotlib.patches.make_path_regular
* pylab.matplotlib.patches.make_wedged_bezier2
* pylab.matplotlib.patches.patchdoc
* pylab.matplotlib.patches.Path
* pylab.matplotlib.patches.PathPatch
* pylab.matplotlib.patches.RegularPolygon
* pylab.matplotlib.patches.Shadow
* pylab.matplotlib.patches.split_bezier_intersecting_with_closedpath
* pylab.matplotlib.patches.split_path_inout
* pylab.matplotlib.patches.transforms

AXES3D
======

============================================ ============================================ ============================================
============================================ ============================================ ============================================
Axes3D._3d_extend_contour                    Axes3D.get_legend_handles_labels             Axes3D.__reduce_ex__
Axes3D.acorr                                 Axes3D.get_lines                             Axes3D.relim
Axes3D.add_artist                            Axes3D.get_navigate                          Axes3D.remove
Axes3D.add_callback                          Axes3D.get_navigate_mode                     Axes3D.remove_callback
Axes3D.add_collection                        Axes3D.get_picker                            Axes3D.__repr__
Axes3D.add_collection3d                      Axes3D.get_position                          Axes3D.reset_position
Axes3D.add_line                              Axes3D.get_proj                              Axes3D.scatter
Axes3D.add_patch                             Axes3D.get_rasterization_zorder              Axes3D.scatter3D
Axes3D.add_table                             Axes3D.get_rasterized                        Axes3D.semilogx
Axes3D.aname                                 Axes3D.get_renderer_cache                    Axes3D.semilogy
Axes3D.annotate                              Axes3D.get_shared_x_axes                     Axes3D.set
Axes3D.apply_aspect                          Axes3D.get_shared_y_axes                     Axes3D.set_adjustable
Axes3D.arrow                                 Axes3D.get_snap                              Axes3D.set_alpha
Axes3D.autoscale_view                        Axes3D.get_tightbbox                         Axes3D.set_anchor
Axes3D.auto_scale_xyz                        Axes3D.get_title                             Axes3D.set_animated
Axes3D._Axes__draw_animate                   Axes3D.get_transform                         Axes3D._set_artist_props
Axes3D._Axes__pick                           Axes3D.get_transformed_clip_path_and_affine  Axes3D.set_aspect
Axes3D.axhline                               Axes3D.get_url                               Axes3D.__setattr__
Axes3D.axhspan                               Axes3D.get_visible                           Axes3D.set_autoscale_on
Axes3D.axis                                  Axes3D.get_window_extent                     Axes3D.set_autoscalex_on
Axes3D.axvline                               Axes3D.get_w_lims                            Axes3D.set_autoscaley_on
Axes3D.axvspan                               Axes3D.get_xaxis                             Axes3D.set_axes
Axes3D.bar                                   Axes3D.get_xaxis_text1_transform             Axes3D.set_axes_locator
Axes3D.bar3d                                 Axes3D.get_xaxis_text2_transform             Axes3D.set_axisbelow
Axes3D.barbs                                 Axes3D.get_xaxis_transform                   Axes3D.set_axis_bgcolor
Axes3D.barh                                  Axes3D.get_xbound                            Axes3D.set_axis_off
Axes3D.__base__                              Axes3D.get_xgridlines                        Axes3D.set_axis_on
Axes3D.__bases__                             Axes3D.get_xlabel                            Axes3D.set_clip_box
Axes3D.__basicsize__                         Axes3D.get_xlim                              Axes3D.set_clip_on
Axes3D.boxplot                               Axes3D.get_xlim3d                            Axes3D.set_clip_path
Axes3D.broken_barh                           Axes3D.get_xmajorticklabels                  Axes3D.set_color_cycle
Axes3D._button_press                         Axes3D.get_xminorticklabels                  Axes3D.set_contains
Axes3D._button_release                       Axes3D.get_xscale                            Axes3D.set_cursor_props
Axes3D.__call__                              Axes3D.get_xticklabels                       Axes3D.set_figure
Axes3D.can_zoom                              Axes3D.get_xticklines                        Axes3D.set_frame_on
Axes3D.cla                                   Axes3D.get_xticks                            Axes3D._set_gc_clip
Axes3D.clabel                                Axes3D.get_yaxis                             Axes3D.set_gid
Axes3D.__class__                             Axes3D.get_yaxis_text1_transform             Axes3D.set_label
Axes3D.clear                                 Axes3D.get_yaxis_text2_transform             Axes3D._set_lim_and_transforms
Axes3D.__cmp__                               Axes3D.get_yaxis_transform                   Axes3D.set_lod
Axes3D.cohere                                Axes3D.get_ybound                            Axes3D.set_navigate
Axes3D.connect                               Axes3D.get_ygridlines                        Axes3D.set_navigate_mode
Axes3D.contains                              Axes3D.get_ylabel                            Axes3D.set_picker
Axes3D.contains_point                        Axes3D.get_ylim                              Axes3D.set_position
Axes3D.contour                               Axes3D.get_ylim3d                            Axes3D.set_rasterization_zorder
Axes3D.contour3D                             Axes3D.get_ymajorticklabels                  Axes3D.set_rasterized
Axes3D.contourf                              Axes3D.get_yminorticklabels                  Axes3D.set_snap
Axes3D.contourf3D                            Axes3D.get_yscale                            Axes3D.set_title
Axes3D.convert_xunits                        Axes3D.get_yticklabels                       Axes3D.set_top_view
Axes3D.convert_yunits                        Axes3D.get_yticklines                        Axes3D.set_transform
Axes3D.create_axes                           Axes3D.get_yticks                            Axes3D.set_url
Axes3D.csd                                   Axes3D.get_zlim3d                            Axes3D.set_visible
Axes3D.__delattr__                           Axes3D.get_zorder                            Axes3D.set_xbound
Axes3D._determine_lims                       Axes3D.grid                                  Axes3D.set_xlabel
Axes3D.__dict__                              Axes3D.has_data                              Axes3D.set_xlim
Axes3D.__dictoffset__                        Axes3D.__hash__                              Axes3D.set_xlim3d
Axes3D.disconnect                            Axes3D.have_units                            Axes3D.set_xscale
Axes3D.__doc__                               Axes3D.hexbin                                Axes3D.set_xticklabels
Axes3D.drag_pan                              Axes3D.hist                                  Axes3D.set_xticks
Axes3D.draw                                  Axes3D.hitlist                               Axes3D.set_ybound
Axes3D.draw_artist                           Axes3D.hlines                                Axes3D.set_ylabel
Axes3D.end_pan                               Axes3D.hold                                  Axes3D.set_ylim
Axes3D.errorbar                              Axes3D.imshow                                Axes3D.set_ylim3d
Axes3D.fill                                  Axes3D.in_axes                               Axes3D.set_yscale
Axes3D.fill_between                          Axes3D.__init__                              Axes3D.set_yticklabels
Axes3D.fill_betweenx                         Axes3D._init_axis                            Axes3D.set_yticks
Axes3D.findobj                               Axes3D.invert_xaxis                          Axes3D.set_zlabel
Axes3D.__flags__                             Axes3D.invert_yaxis                          Axes3D.set_zlim3d
Axes3D.format_coord                          Axes3D.is_figure_set                         Axes3D.set_zorder
Axes3D.format_xdata                          Axes3D.ishold                                Axes3D._shade_colors
Axes3D.format_ydata                          Axes3D.is_transform_set                      Axes3D._shared_x_axes
Axes3D.format_zdata                          Axes3D.__itemsize__                          Axes3D._shared_y_axes
Axes3D.frame                                 Axes3D.legend                                Axes3D.specgram
Axes3D._gen_axes_patch                       Axes3D.loglog                                Axes3D.spy
Axes3D._gen_axes_spines                      Axes3D.matshow                               Axes3D.start_pan
Axes3D._generate_normals                     Axes3D.minorticks_off                        Axes3D.stem
Axes3D.get_adjustable                        Axes3D.minorticks_on                         Axes3D.step
Axes3D.get_alpha                             Axes3D.__module__                            Axes3D.__str__
Axes3D.get_anchor                            Axes3D.mouse_init                            Axes3D.__subclasses__
Axes3D.get_animated                          Axes3D.mro                                   Axes3D.table
Axes3D.get_aspect                            Axes3D.__mro__                               Axes3D.text
Axes3D.__getattribute__                      Axes3D.name                                  Axes3D.text3D
Axes3D.get_autoscale_on                      Axes3D.__name__                              Axes3D.ticklabel_format
Axes3D.get_autoscalex_on                     Axes3D.__new__                               Axes3D.tunit_cube
Axes3D.get_autoscaley_on                     Axes3D._on_move                              Axes3D.tunit_edges
Axes3D.get_axes                              Axes3D.panpy                                 Axes3D.twinx
Axes3D.get_axes_locator                      Axes3D.pany                                  Axes3D.twiny
Axes3D.get_axisbelow                         Axes3D.pchanged                              Axes3D.unit_cube
Axes3D.get_axis_bgcolor                      Axes3D.pcolor                                Axes3D.update
Axes3D.get_axis_position                     Axes3D._pcolorargs                           Axes3D.update_datalim
Axes3D.get_child_artists                     Axes3D.pcolorfast                            Axes3D.update_datalim_bounds
Axes3D.get_children                          Axes3D.pcolormesh                            Axes3D.update_datalim_numerix
Axes3D.get_clip_box                          Axes3D.pick                                  Axes3D.update_from
Axes3D.get_clip_on                           Axes3D.pickable                              Axes3D._update_line_limits
Axes3D.get_clip_path                         Axes3D.pie                                   Axes3D._update_patch_limits
Axes3D.get_contains                          Axes3D.plot                                  Axes3D._update_transScale
Axes3D.get_cursor_props                      Axes3D.plot3D                                Axes3D.view_init
Axes3D.get_data_ratio                        Axes3D.plot_date                             Axes3D.vlines
Axes3D.get_data_ratio_log                    Axes3D.plot_surface                          Axes3D.__weakref__
Axes3D.get_figure                            Axes3D.plot_wireframe                        Axes3D.__weakrefoffset__
Axes3D.get_frame                             Axes3D._process_unit_info                    Axes3D.x
Axes3D.get_frame_on                          Axes3D.properties                            Axes3D.xaxis_date
Axes3D.get_gid                               Axes3D.psd                                   Axes3D.xaxis_inverted
Axes3D.get_images                            Axes3D.quiver                                Axes3D.xcorr
Axes3D.get_label                             Axes3D.quiverkey                             Axes3D.yaxis_date
Axes3D.get_legend                            Axes3D.redraw_in_frame                       Axes3D.yaxis_inverted
Axes3D._get_legend_handles                   Axes3D.__reduce__                            Axes3D.zorder
============================================ ============================================ ============================================
