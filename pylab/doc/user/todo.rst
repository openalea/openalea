
Implementation
###############


.. topic:: target

    This page is for developers only


.. contents::


How to generate this documentation
====================================

::

    cd doc
    make html

Since openalea.pylab is based upon matplotlib/pylab, we can take advantage of a sphinx extension provided 
within the matplotlib library called **plot_directive**, which works as follows. If you include 
a valid pylab code as follows::

    .. plot:: 

        from pylab import *
        plot(randn(100), randn(100), 'or')

then sphinx generates the following image and include it in your final HTML version:

.. plot:: 

    from pylab import *
    plot(randn(100), randn(100), 'or')

Then, within VisuAlea (in the openalea.misc package), we developed a sphinx extension that allows to include a VisuAlea dataflow. It works as follows::

    .. dataflow:: openalea.pylab.demo scatter_and_histograms

where **openalea.pylab.demo** is your wralea package name and **scatter_and_histograms** the name of your composite node.

.. dataflow:: openalea.pylab.demo scatter_and_histograms

.. warning:: Issue with the dataflow extension (about 20% of the dataflow generated do not show the edges
.. warning:: Issue with the plot_directive extension. Before compiling the documentation, you must edit the openalea.pylab.plotting.py_pylab.py file to comment the code within the  *update_figure* method in the class *Plotting*. Otherwise you will obtain a single figure (if several are requested). Also in the colorBar class, you need to comment figure.canvas.draw() at the end of the class code.

API
====
First input and output node connectors are reserved !!
-------------------------------------------------------

Let us consider the following example where we plot a x,y data sets.
::

    from pylab import *
    x = arange(0, 10, 0.1)
    y = x*x
    plot(x,y)
    show()

In principle, you should tell in which figure you want to plot the result::

    from pylab import *
    x = arange(0, 10, 0.1)
    y = x*x
    figure(1)
    plot(x,y)
    show()


.. note:: In VisuAlea all plotting nodes must have a connector to specify the figure id where
    data should be plotted.


Yet, within a figure, you may want to place several axes that are independent.
So, you should really be able to do is to specify the axes as well::

    from pylab import *
    x = arange(0, 10, 0.1)
    y = x*x
    figure(1)
    ax = gca()
    plot(x,y)
    show()


so that later on, you can get back a particular axe to add labels or title::


    from pylab import *
    x = arange(0, 10, 0.1)
    y = x*x
    figure(1)
    ax = gca()
    plot(x,y)

    figure(2)
    plot(x,y)

    sca(ax)
    title('my first axe in the figure 1')
    show()


.. note:: In VisuAlea, each node that plots data (or adjusts and manipulate an axe) should
    keep track of the axe it is related to. The first input connector is used to get
    an axes object. If connected, the data will be plotted inside this input axes. If not,
    if the node is called for the first time, it creates a new axe. If the node was already called,
    then then the axes is cleared.

arguments
------------------

Plotting functions have most of their arguments available within VisuAlea. Usually they appear as connectors
in the same order as in pylab documentation.

.. warning:: the last connector should be a kwargs to take as much argument as needed. This is especially important if
   the pylab api changes, or you do not want to add too many connectors.


to be added in Visualea
========================

=============== ========================================================
Function         Description
=============== ========================================================
quiverkey       that takes as input the output of quiver node. Add
                legend with quiver arrow legend.
spy             plot sparsity pattern using markers or image
hlines
twinx
plot_date
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
ioff            turn interaction mode off
ion             turn interaction mode on
isinteractive   return True if interaction mode is on
imread          load image file into array
imsave          save array as an image file
ishold          return the hold state of the current axes
matshow         display a matrix in a new figure preserving aspect
plotfile        plot column data from an ASCII tab/space/comma delimited file
rc              control the default params
rgrids          customize the radial grids and labels for polar
setp            set a graphics property
table           add a table to the plot
thetagrids      customize the radial theta grids and labels for polar
=============== ========================================================




pylab functions to be implemented in openalea.numpy or openalea.pylab ?
========================================================================
.. pylab.hypergeometric           pylab.nan_to_num               pylab.select    pylab.nbytes
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
    ylab.amap                     pylab.dist                     pylab.imsave                   pylab.NINF                     pylab.setp
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
    pylab.plot_date
     pylab.isfinite                 pylab.plotfile
    b.average                  pylab.fastCopyAndTranspose                     pylab.plotting
    pylab.ishold                   pylab.plt                      pylab.stineman_interp
    pylab.isinf                    pylab.pmt
    pylab.barbs                    pylab.figaspect                pylab.isreal                   pylab.poly_below               pylab.subplots_adjust
    pylab.barh                     pylab.isrealobj                pylab.poly_between             pylab.subplot_tool
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
    pylab.FPE_UNDERFLOW            pylab.LogFormatterExponent     pylab.typeDict
      pylab.FR                       pylab.LogFormatterMathtext     pylab.typeNA
    pylab.choose                   pylab.frange                   pylab.rc                       pylab.typename
    pylab.rcdefaults               pylab.ubyte
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
    pyla    b.connect                  pylab.get_numarray_include     pylab.may_share_memory         pylab.rfft2                    pylab.vlines
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
    pylab.DAILY                      pylab.mpl                  
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
axes3d
============================================ ============================================ ============================================
Axes3D.acorr                                                         m
Axes3D.add_callback
Axes3D.add_collection
Axes3D.add_collection3d
Axes3D.add_line                             
Axes3D.scatter
Axes3D.add_patch  
Axes3D.scatter3D
Axes3D.add_table   
Axes3D.semilogx
Axes3D.aname  
Axes3D.semilogy
Axes3D.annotate
Axes3D.arrow
Axes3D.axhline
Axes3D.axhspan
Axes3D.axis
Axes3D.axvline
Axes3D.axvspan
Axes3D.bar
Axes3D.bar3d
Axes3D.barbs
Axes3D.barh
Axes3D.cla
Axes3D.clabel
Axes3D.cohere
Axes3D.connect
Axes3D.contains
Axes3D.contains_point
Axes3D.convert_xunits
Axes3D.convert_yunits
Axes3D.create_axes
Axes3D.csd
Axes3D.grid
Axes3D.hexbin
Axes3D.hist
Axes3D.hitlist
Axes3D.hlines
Axes3D.end_pan
Axes3D.errorbar
Axes3D.imshow
Axes3D.fill
Axes3D.fill_between
Axes3D.fill_betweenx
Axes3D.frame
Axes3D.legend
Axes3D.specgram
Axes3D.loglog
Axes3D.spy
Axes3D.matshow
Axes3D.start_pan
Axes3D.stem
Axes3D.step
Axes3D.table
Axes3D.text
Axes3D.text3D
Axes3D.ticklabel_format
Axes3D.tunit_cube
Axes3D.tunit_edges
Axes3D.panpy
Axes3D.twinx
Axes3D.pany
Axes3D.twiny
Axes3D.pchanged
Axes3D.pcolor
Axes3D.pcolorfast
Axes3D.pcolormesh
Axes3D.pick
Axes3D.pickable
Axes3D.pie
Axes3D.plot
Axes3D.plot3D
Axes3D.plot_date
Axes3D.plot_surface
Axes3D.plot_wireframe
Axes3D._process_unit_info
Axes3D.properties
Axes3D.psd
Axes3D.quiver
Axes3D.xcorr
Axes3D.quiverkey
============================================ ============================================ ============================================
