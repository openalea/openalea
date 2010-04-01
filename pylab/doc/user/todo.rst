Available as a visualea node
=============================

subplot versus axes
--------------------



=============== ========================================================
iplotting Func  Description
=============== ========================================================
acorr           plot the autocorrelation function
bar             make a bar chart
boxplot         make a box and whisker plot
hist            make a histogram 
hexbin          make a 2D hexagonal binning plot
plot            make a line plot
scatter         make a scatter plot
polar           make a polar plot on a PolarAxes
pie             pie charts
loglog          a log log plot
subplot         make a subplot (numrows, numcols, axesnum)
contour         make a contour plot
contourf        make a filled contour plot
csd             make a plot of cross spectral density
psd             make a plot of power spectral density
specgram        a spectrogram plot
semilogx        log x axis
semilogy        log y axis
stem            make a stem plot
pcolor          make a pseudocolor plot
pcolormesh      make a pseudocolor plot using a quadrilateral mesh
step 
=============== ========================================================


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


=============== ========================================================
classes
=============== ========================================================
line2D          used by plot functions
fontproperties  used by text functions
=============== ========================================================



=============== ========================================================
Function         Description
=============== ========================================================
random          calls pylab.random
absolute        calls numpy.absolute
arange
meshgrid
=============== ========================================================

to be add in Visualea
=====================


=============== ========================================================
Function         Description
=============== ========================================================
arrow           add an arrow to the axes
barbs           a (wind) barb plot
barh            a horizontal bar chart
broken_barh     a set of horizontal bars with gaps
clf             clear a figure window
clim            adjust the color limits of the current image
close           close a figure window
delaxes         delete an axes from the current figure
draw            Force a redraw of the current figure
errorbar        make an errorbar graph
figlegend       make legend on the figure rather than the axes
figimage        make a figure image
figtext         add text in figure coords
fill            make filled polygons
fill_between    make filled polygons between two curves
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
imshow          plot image data
ishold          return the hold state of the current axes
matshow         display a matrix in a new figure preserving aspect
plot_date       plot dates
plotfile        plot column data from an ASCII tab/space/comma delimited file
quiver          make a direction field (arrows) plot
rc              control the default params
rgrids          customize the radial grids and labels for polar
setp            set a graphics property
show            show the figures
spy             plot sparsity pattern using markers or image
table           add a table to the plot
thetagrids      customize the radial theta grids and labels for polar
xcorr           plot the autocorrelation function of x and y
=============== ========================================================



=============== =========================================================
Command         Description
=============== =========================================================
clf             clear a figure window
close           close a figure window
draw            force a redraw of the current figure
errorbar        make an errorbar graph
figlegend       add a legend to the figure
figimage        add an image to the figure, w/o resampling
figtext         add text in figure coords
fill            make filled polygons
fill_between    make filled polygons between two sets of y-values
fill_betweenx   make filled polygons between two sets of x-values
gca             return the current axes
gcf             return the current figure
gci             get the current image, or None
getp            get a graphics property
imread          load image file into array
imsave          save array as an image file
imshow          plot image data
matshow         display a matrix in a new figure preserving aspect
plotfile        plot data from a flat file
quiver          make a direction field (arrows) plot
rc              control the default params
setp            set a graphics property
show            show the figures
table           add a table to the axes
=============== =========================================================



pylab functions
================i



pylab.hypergeometric           pylab.nan_to_num               pylab.select
       pylab.nbytes 
pylab.add                      pylab.i0                       pylab.ndarray 
pylab.add_docstring            pylab.identity                 pylab.ndenumerate              
pylab.add_newdoc                                   pylab.ifft                     pylab.ndim                     pylab.setbufsize
pylab.add_newdocs              pylab.diagflat                 pylab.ifft2                    pylab.ndindex                  
pylab.alen                     pylab.diagonal                 pylab.ifftn                    pylab.negative                 pylab.setdiff1d
pylab.all                      pylab.ifftshift                pylab.negative_binomial        pylab.seterr
pylab.allclose                      pylab.ihfft                    .seterrcall
pylab.ALLOW_THREADS            pylab.digitize                 pylab.iinfo                    pylab.newaxis                  pylab.seterrobj
pylab.alltrue                  pylab.disconnect               pylab.imag                     pylab.newbuffer                pylab.setmember1d
pylab.alterdot                 pylab.disp                     pylab.imread                   pylab.new_figure_manager       pylab.set_numeric_ops
pylab.amap                     pylab.dist                     pylab.imsave                   pylab.NINF                     pylab.setp
pylab.amax                     pylab.distances_along_curve    pylab.imshow                   pylab.noncentral_chisquare     pylab.set_printoptions
pylab.amin                     pylab.dist_point_to_segment    pylab.IndexDateFormatter       pylab.noncentral_f             pylab.set_state
pylab.angle                    pylab.divide                   pylab.index_exp                pylab.nonzero                  pylab.set_string_function
pylab.IndexLocator             pylab.norm                     pylab.setxor1d
pylab.Annotation                                  pylab.indices                  pylab.normal                   pylab.shape
pylab.any                      pylab.double                   pylab.inexact                  pylab.normalize                
pylab.append                   pylab.drange                   pylab.inf                      pylab.Normalize              
pylab.apply_along_axis         pylab.draw                     pylab.Inf                      pylab.norm_flat               
pylab.apply_over_axes          pylab.draw_if_interactive      pylab.Infinity                 pylab.normpdf               
pylab.dsplit                   pylab.info                     pylab.not_equal                pylab.short
pylab.dstack                   pylab.infty                    pylab.np                       pylab.show
pylab.nper                     pylab.show_config
pylab.inner                    pylab.npv                      pylab.shuffle
pylab.ediff1d                  pylab.insert                   pylab.NullFormatter            pylab.sign
pylab.eig                      pylab.inside_poly              pylab.NullLocator              pylab.signbit
pylab.eigh                     pylab.int_                     pylab.num2date                 pylab.signedinteger
pylab.eigvals                  pylab.int0                     pylab.num2epoch                pylab.silent_list
pylab.argmax                   pylab.eigvalsh                 pylab.int16                    pylab.number               
pylab.argmin                   pylab.emath                    pylab.int32                    pylab.NZERO               pylab.sinc
pylab.argsort                                  pylab.int64                    pylab.obj2sctype               pylab.single
pylab.argwhere                 pylab.empty_like               pylab.int8                     pylab.object_                  pylab.singlecomplex
pylab.around                   pylab.entropy                  pylab.int_asbuffer             pylab.object0            
pylab.array                    pylab.epoch2num                pylab.intc                     pylab.ogrid                    pylab.size
pylab.array2string             pylab.equal                    pylab.integer                                    pylab.Slider
pylab.array_equal              pylab.ERR_CALL                 pylab.interactive              pylab.ones_like                pylab.slopes
pylab.array_equiv              pylab.ERR_DEFAULT              pylab.interp                                       pylab.solve
pylab.array_repr               pylab.ERR_DEFAULT2             pylab.intersect1d              pylab.over                     pylab.sometrue
pylab.array_split              pylab.ERR_IGNORE               pylab.intersect1d_nu           pylab.PackageLoader            pylab.sort
pylab.array_str                pylab.ERR_LOG                  pylab.intp                     pylab.packbits                 pylab.sort_complex
pylab.arrow                    pylab.errorbar                                      pylab.pareto                   pylab.source
pylab.Arrow                    pylab.ERR_PRINT                pylab.invert                   pylab.path_length           
pylab.Artist                   pylab.ERR_RAISE                pylab.ioff                     
pylab.asanyarray               pylab.errstate                 pylab.ion                      pylab.split
pylab.asarray                  pylab.ERR_WARN                 pylab.ipmt                     pylab.permutation             p
pylab.asarray_chkfinite        pylab.exception_to_str         pylab.irefft                   pylab.pi                       pylab.spy
pylab.ascontiguousarray                              pylab.irefft2                
pylab.asfarray                 pylab.expand_dims              pylab.irefftn                  pylab.piecewise              
pylab.asfortranarray           pylab.expm1                    pylab.irfft                    pylab.PINF                     pylab.squeeze
pylab.asmatrix                 pylab.exponential              pylab.irfft2                                        pylab.standard_cauchy
pylab.asscalar                 pylab.exp_safe                 pylab.irfftn                   pylab.pinv                     pylab.standard_exponential
pylab.atleast_1d               pylab.extract                  pylab.irr                      pylab.pkgload                  pylab.standard_gamma
pylab.atleast_2d                    pylab.is_closed_polygon        pylab.place                    pylab.standard_normal
pylab.atleast_3d               pylab.f                        pylab.iscomplex                pylab.plot                     pylab.standard_t
pylab.AutoLocator              pylab.fabs                     pylab.iscomplexobj             pylab.plot_date                pylab.std
ylab.False_                   pylab.isfinite                 pylab.plotfile                
b.average                  pylab.fastCopyAndTranspose                     pylab.plotting                 
pylab.fft                      pylab.ishold                   pylab.plt                      pylab.stineman_interp
pylab.fft2                     pylab.isinf                    pylab.pmt                     
pylab.fftfreq                  pylab.isinteractive            pylab.poisson                  pylab.str_
pylab.fftn                     pylab.isnan                    pylab.polar                    pylab.string_
pylab.fftpack                  pylab.isneginf                 pylab.PolarAxes                pylab.string0
pylab.fftpack_lite             pylab.is_numlike               pylab.poly                     pylab.strpdate2num
pylab.fftshift                 pylab.isposinf                 pylab.poly1d                   pylab.SU
pylab.bar                      pylab.fftsurr                  pylab.ispower2                 pylab.polyadd                  pylab.subplot
pylab.barbs                    pylab.figaspect                pylab.isreal                   pylab.poly_below               pylab.subplots_adjust
pylab.barh                     pylab.figimage                 pylab.isrealobj                pylab.poly_between             pylab.subplot_tool
pylab.figlegend                pylab.isscalar                 pylab.polyder                  pylab.SubplotTool
pylab.base_repr                pylab.fignum_exists            pylab.issctype                 pylab.polydiv                  pylab.subtract
pylab.bench                    pylab.figtext                  pylab.is_string_like           pylab.polyfit                  pylab.sum
pylab.beta                     pylab.figure                   pylab.issubclass_              pylab.Polygon                  
pylab.binary_repr              pylab.Figure                   pylab.issubdtype               pylab.polyint                  pylab.suptitle
pylab.bincount                 pylab.FigureCanvasBase         pylab.issubsctype              pylab.polymul                  pylab.svd
pylab.binomial                  pylab.isvector                 pylab.polysub                  pylab.swapaxes
pylab.bitwise_and              pylab.fill                     pylab.iterable                 pylab.polyval                  pylab.switch_backend
pylab.bitwise_not              pylab.fill_between             pylab.ix_                      pylab.power                    pylab.sys
pylab.bitwise_or               pylab.fill_betweenx                                 pylab.ppmt                     pylab.table
pylab.bitwise_xor              pylab.find                     pylab.prctile                  pylab.take
pylab.bivariate_normal         pylab.find_common_type         pylab.kron                     pylab.prctile_rank          
pylab.findobj                  pylab.l1norm                   pylab.prepca                  
pylab.bmat                     pylab.finfo                    pylab.l2norm                                       pylab.tensordot
pylab.bone                     pylab.fix                      pylab.lapack_lite              pylab.prod                     pylab.tensorinv
pylab.bool_                    pylab.FixedFormatter           pylab.laplace                  pylab.product                  pylab.tensorsolve
pylab.bool8                    pylab.FixedLocator             pylab.ldexp                    pylab.test
pylab.flag                     pylab.left_shift               pylab.ptp                      pylab.Tester
pylab.flatiter                 pylab.legend                   pylab.put                      pylab.text
pylab.broadcast                pylab.flatnonzero              pylab.less                                       pylab.Text
pylab.broadcast_arrays         pylab.flatten                  pylab.less_equal               pylab.pv                       pylab.TH
pylab.broken_barh              pylab.flexible                 pylab.levypdf                  pylab.pylab_setup              pylab.thetagrids
            pylab.fliplr                   pylab.lexsort                  pylab.PZERO                    pylab.TickHelper
    pylab.flipud                   pylab.liaupunov                pylab.qr                       pylab.tile
pylab.Button                   pylab.float_                   pylab.linalg                   pylab.quiver                   pylab.title
pylab.byte                     pylab.float32                  pylab.LinAlgError              pylab.quiverkey                pylab.trace
pylab.byte_bounds              pylab.float64                  pylab.r_                       pylab.transpose
pylab.bytes                    pylab.float96                  pylab.LinearLocator            pylab.radians                  pylab.trapz
pylab.c_                       pylab.floating                               pylab.RAISE            
pylab.can_cast                 pylab.FLOATING_POINT_SUPPORT   pylab.little_endian            pylab.rand                     pylab.triangular
pylab.cast                     pylab.floor                    pylab.load                     pylab.randint                
pylab.cbook                    pylab.floor_divide             pylab.loads                    pylab.trim_zeros
pylab.cdouble                  pylab.fmod                     pylab.loadtxt               
 pylab.format_parser            pylab.Locator                  pylab.random_integers          pylab.True_
pylab.center_matrix            pylab.FormatStrFormatter                             pylab.random_sample            pylab.true_divide
pylab.cfloat                   pylab.Formatter                                    pylab.ranf                     pylab.TU
pylab.char                     pylab.FPE_DIVIDEBYZERO         pylab.log1p                    pylab.rank                     pylab.twinx
pylab.character                pylab.FPE_INVALID              pylab.log2                     pylab.RankWarning              pylab.twiny
pylab.chararray                pylab.FPE_OVERFLOW             pylab.LogFormatter             pylab.rate                     pylab.typecodes
pylab.chisquare                pylab.FPE_UNDERFLOW            pylab.LogFormatterExponent     pylab.ravel                    pylab.typeDict
pylab.cholesky                 pylab.FR                       pylab.LogFormatterMathtext     pylab.rayleigh                 pylab.typeNA
pylab.choose                   pylab.frange                   pylab.logical_and              pylab.rc                       pylab.typename
pylab.Circle                   pylab.frexp                    pylab.logical_not              pylab.rcdefaults               pylab.ubyte
pylab.frombuffer               pylab.logical_or               pylab.rcParams                 pylab.ufunc
pylab.fromfile                 pylab.logical_xor              pylab.rcParamsDefault          pylab.UFUNC_BUFSIZE_DEFAULT
pylab.fromfunction             pylab.logistic                 pylab.real                     pylab.UFUNC_PYVALS_NAME
pylab.clf                      pylab.fromiter                 pylab.LogLocator               pylab.real_if_close            pylab.uint
pylab.clim                     pylab.frompyfunc               pylab.rec                      pylab.uint0
pylab.clip                     pylab.fromregex                pylab.lognormal                pylab.rec2csv                  pylab.uint16
pylab.CLIP                     pylab.fromstring               pylab.logseries                pylab.rec_append_fields        pylab.uint32
pylab.clongdouble              pylab.FuncFormatter                         pylab.recarray                 pylab.uint64
pylab.clongfloat               pylab.fv                       pylab.longcomplex              pylab.rec_drop_fields          pylab.uint8
pylab.close                    pylab.gamma                    pylab.longdouble               pylab.reciprocal               pylab.uintc
pylab.cm                       pylab.gca                      pylab.longest_contiguous_ones  pylab.rec_join                 pylab.uintp
pylab.cohere                   pylab.gcf                      pylab.longest_ones             pylab.record                   pylab.ulonglong
  pylab.gci                      pylab.longfloat                pylab.Rectangle                pylab.unicode_
pylab.colormaps                pylab.generic                  pylab.longlong                
pylab.colors                   pylab.geometric                pylab.lookfor                   pylab.uniform
pylab.column_stack             pylab.get                      pylab.lstsq                    pylab.refft                    pylab.union1d
pylab.common_type              pylab.get_array_wrap           pylab.ma                       pylab.refft2                   pylab.unique
pylab.compare_chararrays       pylab.MachAr                   pylab.refftn                   pylab.unique1d
pylab.complex_                 pylab.get_backend              pylab.mat                      pylab.register_cmap            pylab.unpackbits
pylab.complex128               pylab.getbuffer                pylab.math                     pylab.relativedelta            pylab.unravel_index
pylab.complex192               pylab.getbufsize               pylab.matplotlib               pylab.remainder                pylab.unsignedinteger
pylab.complex64                pylab.get_cmap                 pylab.matrix                   pylab.repeat                   pylab.unwrap
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
pylab.cool                     pylab.get_printoptions                        pylab.vsplit
pylab.copper                   pylab.get_scale_docs           pylab.mgrid                    pylab.rk4                      pylab.vstack
pylab.copy                     pylab.get_scale_names          pylab.minimum                  pylab.rms_flat                 pylab.waitforbuttonpress
pylab.corrcoef                 pylab.get_sparse_matrix        pylab.minorticks_off           pylab.roll                     pylab.wald
pylab.correlate                pylab.get_state                pylab.minorticks_on            pylab.rollaxis                 pylab.warnings
pylab.get_xyz_where            pylab.mintypecode              pylab.roots                    pylab.WE
                pylab.ginput                   pylab.MinuteLocator            pylab.rot90                    pylab.WeekdayLocator
pylab.cov                      pylab.gradient                 pylab.MINUTELY                 pylab.round_                   pylab.WEEKLY
   pylab.gray                     pylab.mirr                     pylab.row_stack                pylab.weibull
ylab.greater                  pylab.mlab                     pylab.rrule                    pylab.where
pylab.csingle                  pylab.greater_equal            pylab.MO                       pylab.RRuleLocator             pylab.who
pylab.csv2rec                                      pylab.mod                      pylab.s_                       pylab.Widget
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
pylab.delaxes                  pylab.hot                      pylab.NAN                      pylab.sctypes                  pylab.yticks
pylab.delete                   pylab.HourLocator              pylab.nanargmax                pylab.searchsorted             pylab.zeros
pylab.demean                   pylab.HOURLY                   pylab.nanargmin                pylab.SecondLocator            pylab.zeros_like
pylab.deprecate                pylab.hsplit                   pylab.nanmax                   pylab.SECONDLY                 pylab.zipf
pylab.deprecate_with_doc       pylab.hstack                   pylab.nanmin                   pylab.seed                     
pylab.det                      pylab.hsv                      pylab.nansum                   pylab.segments_intersec






pylab.matplotlib.afm                     pylab.matplotlib.distutils               pylab.matplotlib._mathtext_data          
pylab.matplotlib.artist                  pylab.matplotlib.matplotlib_fname        
pylab.matplotlib.minor1                 
pylab.matplotlib.minor2                
pylab.matplotlib.backend_bases           pylab.matplotlib.finance                 pylab.matplotlib.s
pylab.matplotlib.backends                pylab.matplotlib.fontconfig_pattern      pylab.matplotlib.mpl                     pylab.matplotlib.scale
pylab.matplotlib.bezier                  pylab.matplotlib.font_manager            
pylab.matplotlib.blocking_input          pylab.matplotlib.ft2font                 pylab.matplotlib.shutil
pylab.matplotlib.generators              pylab.matplotlib.NEWCONFIG               pylab.matplotlib.spines
pylab.matplotlib.cbook                   pylab.matplotlib.nn                  
pylab.matplotlib.checkdep_dvipng         pylab.matplotlib.get_backend           
pylab.matplotlib.checkdep_ghostscript    pylab.matplotlib.nxutils                 
pylab.matplotlib.checkdep_pdftops        pylab.matplotlib.get_configdir           pylab.matplotlib.offsetbox               pylab.matplotlib.table
pylab.matplotlib.checkdep_ps_distiller                    pylab.matplotlib.tempfile
pylab.matplotlib.checkdep_tex            pylab.matplotlib.get_data_path           pylab.matplotlib.patches                 pylab.matplotlib.text
pylab.matplotlib.checkdep_usetex         pylab.matplotlib.path                    pylab.matplotlib.ticker
pylab.matplotlib.get_example_data        pylab.matplotlib.tight_bbox
         .matplotlib.tk_window_focus
pylab.matplotlib.get_home                pylab.matplotlib.tmp
pylab.matplotlib.get_py2exe_datafiles    pylab.matplotlib.projections             pylab.matplotlib.transforms
pylab.matplotlib.collections             pylab.matplotlib.pylab                   pylab.matplotlib.units
pylab.matplotlib.use
pylab.matplotlib.colors                  pylab.matplotlib.image                   pylab.matplotlib.pyparsing              
pylab.matplotlib.compare_versions        pylab.matplotlib.pyplot                  pylab.matplotlib.validate_backend
pylab.matplotlib.validate_cairo_format
pylab.matplotlib.converter               pylab.matplotlib.interactive            ylab.matplotlib.validate_toolbar
pylab.matplotlib.is_interactive          pylab.matplotlib.rc                      
pylab.matplotlib.dates                   pylab.matplotlib.is_string_like          pylab.matplotlib.rcdefaults             
pylab.matplotlib.default                 pylab.matplotlib.rc_params          
pylab.matplotlib.defaultParams           pylab.matplotlib.key                     pylab.matplotlib.rcParams             
pylab.matplotlib.legend                  pylab.matplotlib.RcParams                pylab.matplotlib.widgets
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
pylab.matplotlib.mlab.isvector                          
pylab.matplotlib.mlab.kwdocd                            pylab.matplotlib.mlab.rk4
pylab.matplotlib.mlab.l1norm                            pylab.matplotlib.mlab.rms_flat
pylab.matplotlib.mlab.l2norm                            pylab.matplotlib.mlab.safe_isinf
pylab.matplotlib.mlab.less_simple_linear_interpolation  pylab.matplotlib.mlab.safe_isnan
pylab.matplotlib.mlab.dist                              pylab.matplotlib.mlab.levypdf                           pylab.matplotlib.mlab.save
pylab.matplotlib.mlab.distances_along_curve             pylab.matplotlib.mlab.liaupunov                         pylab.matplotlib.mlab.segments_intersect
pylab.matplotlib.mlab.dist_point_to_segment             pylab.matplotlib.mlab.load                              
pylab.matplotlib.mlab.division                          pylab.matplotlib.mlab.log2                              pylab.matplotlib.mlab.slopes
 
pylab.matplotlib.mlab.donothing_callback                pylab.matplotlib.mlab.longest_contiguous_ones          p
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
matplotlib.axes                    matplotlib.defaultParams           matplotlib.image                   matplotlib.path                    matplotlib.spines
matplotlib.axis                   
matplotlib.backend_bases         matplotlib.subprocess
matplotlib.backends              .interactive             matplotlib.sys
matplotlib.bezier                matplotlib.is_interactive          matplotlib.projections             matplotlib.table
matplotlib.blocking_input          matplotlib.distutils               matplotlib.is_string_like          matplotlib.pylab                   matplotlib.tempfile
matplotlib.text
matplotlib.cbook                   matplotlib.figure                  matplotlib.key                     matplotlib.pyparsing               matplotlib.ticker
matplotlib.checkdep_dvipng       matplotlib.legend                  matplotlib.pyplot                  matplotlib.tight_bbox
matplotlib.checkdep_ghostscript    matplotlib.finance                 matplotlib.lines                   
matplotlib.checkdep_pdftops        matplotlib.fontconfig_pattern      matplotlib.major                   matplotlib.quiver                  matplotlib.tmp
matplotlib.checkdep_ps_distiller   matplotlib.font_manager            matplotlib.mathtext                matplotlib.rc                      matplotlib.transforms
matplotlib.checkdep_tex            matplotlib.ft2font                 matplotlib.rcdefaults              matplotlib.units
matplotlib.checkdep_usetex         matplotlib.generators              matplotlib.matplotlib_fname        matplotlib.rc_params               matplotlib.use
matplotlib.minor1                  matplotlib.rcParams                
matplotlib.cm                      matplotlib.get_backend             matplotlib.minor2                  matplotlib.RcParams                matplotlib.validate_backend
matplotlib.mlab                    matplotlib.rcParamsDefault         matplotlib.validate_cairo_format
matplotlib.get_configdir           matplotlib.mpl                     matplotlib.rcsetup                 matplotlib.validate_toolbar
matplotlib.collections           matplotlib.re                      
matplotlib.get_data_path          
matplotlib.NEWCONFIG               
matplotlib.compare_versions        matplotlib.get_example_data        matplotlib.nn                   
 matplotlib.widgets
matplotlib.get_home                matplotlib.nxutils                 matplotlib.s                       
matplotlib.get_py2exe_datafiles    matplotlib.offsetbox               matplotlib.scale                


 cumsum    - the cumulative sum along a dimension
      eig       - the eigenvalues and eigen vectors of v
      find      - return the indices where a condition is nonzero
      fliplr    - flip the rows of a matrix up/down
      flipud    - flip the columns of a matrix left/right
      rand      - an array from the uniform distribution [0,1]
      rot90     - rotate matrix k*90 degress counterclockwise
      squeeze   - squeeze an array removing any dimensions of length 1
      svd       - singular value decomposition
      zeros     - a matrix of zeros

   _Probability
    
      levypdf   - The levy probability density function from the char. func.
      normpdf   - The Gaussian probability density function
      rand      - random numbers from the uniform distribution
    
    _Statistics
    
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
    


   _Time series analysis
    
      fft       - the fast Fourier transform of vector x
      hist      - compute the histogram of x
      sinc      - the sinc function of array x
    
    _Dates
    
      date2num  - convert python datetimes to numeric representation
      drange    - create an array of numbers for date plots
      num2date  - convert numeric type (float days since 0001) to datetime
    
    _Other
    
      angle     - the angle of a complex array
      griddata  - interpolate irregularly distributed data to a regular grid

   _Other
    
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











pylab.matplotlib.patches.allow_rasterization
pylab.matplotlib.patches.Arc
pylab.matplotlib.patches.Arrow
pylab.matplotlib.patches.ArrowStyle
pylab.matplotlib.patches.artist
pylab.matplotlib.patches.bbox_artist
pylab.matplotlib.patches.BoxStyle

.matplotlib.patches.cbook
pylab.matplotlib.patches.Circle
pylab.matplotlib.patches.CirclePolygon
pylab.matplotlib.patches.colors
pylab.matplotlib.patches.concatenate_paths
pylab.matplotlib.patches.ConnectionPatch
pylab.matplotlib.patches.ConnectionStyle
pylab.matplotlib.patches.division
pylab.matplotlib.patches.draw_bbox
pylab.matplotlib.patches.Ellipse
pylab.matplotlib.patches.FancyArrow
pylab.matplotlib.patches.FancyBboxPatch
pylab.matplotlib.patches.get_cos_sin
pylab.matplotlib.patches.get_intersection
pylab.matplotlib.patches.get_parallels
pylab.matplotlib.patches.inside_circle
pylab.matplotlib.patches.k
pylab.matplotlib.patches.make_path_regular
pylab.matplotlib.patches.make_wedged_bezier2
pylab.matplotlib.patches.math
pylab.matplotlib.patches.mpl
pylab.matplotlib.patches.np
pylab.matplotlib.patches.Patch
pylab.matplotlib.patches.patchdoc
pylab.matplotlib.patches.Path
pylab.matplotlib.patches.PathPatch
pylab.matplotlib.patches.Rectangle
pylab.matplotlib.patches.RegularPolygon
pylab.matplotlib.patches.Shadow
pylab.matplotlib.patches.split_bezier_intersecting_with_closedpath
pylab.matplotlib.patches.split_path_inout
pylab.matplotlib.patches.transforms
pylab.matplotlib.patches.Wedge

