
Available as a visualea node
=============================

=============== ========================================================
iplotting Func  Description
=============== ========================================================
acorr           plot the autocorrelation function
bar             make a bar chart
boxplot         make a box and whisker plot
hist            make a histogram 
plot            make a line plot
scatter         make a scatter plot
polar           make a polar plot on a PolarAxes
pie             pie charts
loglog          a log log plot
=============== ========================================================


=============== ========================================================
text            Description
=============== ========================================================
axes
axis
figure
legend          make an axes legend
xlabel          add an xlabel to the current axes
ylabel          add a ylabel to the current axes
ititle           add a title to the current axes
text            add some text at location x,y to the current axes
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
=============== ========================================================

to be add in Visualea
=====================


=============== ========================================================
Function         Description
=============== ========================================================
annotate        annotate something in the figure
arrow           add an arrow to the axes
axhline         draw a horizontal line across axes
axvline         draw a vertical line across axes
axhspan         draw a horizontal bar across axes
axvspan         draw a vertical bar across axes
barbs           a (wind) barb plot
barh            a horizontal bar chart
broken_barh     a set of horizontal bars with gaps
box             set the axes frame on/off state
cla             clear current axes
clabel          label a contour plot
clf             clear a figure window
clim            adjust the color limits of the current image
close           close a figure window
colorbar        add a colorbar to the current figure
contour         make a contour plot
contourf        make a filled contour plot
csd             make a plot of cross spectral density
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
grid            set whether gridding is on
hexbin          make a 2D hexagonal binning plot
hist            make a histogram
hold            set the axes hold state
ioff            turn interaction mode off
ion             turn interaction mode on
isinteractive   return True if interaction mode is on
imread          load image file into array
imsave          save array as an image file
imshow          plot image data
ishold          return the hold state of the current axes
matshow         display a matrix in a new figure preserving aspect
pcolor          make a pseudocolor plot
pcolormesh      make a pseudocolor plot using a quadrilateral mesh
plot_date       plot dates
plotfile        plot column data from an ASCII tab/space/comma delimited file
psd             make a plot of power spectral density
quiver          make a direction field (arrows) plot
rc              control the default params
rgrids          customize the radial grids and labels for polar
savefig         save the current figure
setp            set a graphics property
semilogx        log x axis
semilogy        log y axis
show            show the figures
specgram        a spectrogram plot
spy             plot sparsity pattern using markers or image
stem            make a stem plot
subplot         make a subplot (numrows, numcols, axesnum)
subplots_adjust change the params controlling the subplot positions of current figure
subplot_tool    launch the subplot configuration tool
suptitle        add a figure title
table           add a table to the plot
thetagrids      customize the radial theta grids and labels for polar
xcorr           plot the autocorrelation function of x and y
xlim            set/get the xlimits
ylim            set/get the ylimits
xticks          set/get the xticks
yticks          set/get the yticks
=============== ========================================================



=============== =========================================================
Command         Description
=============== =========================================================
cla             clear current axes
clabel          label a contour plot
clf             clear a figure window
close           close a figure window
colorbar        add a colorbar to the current figure
contour         make a contour plot
contourf        make a filled contour plot
csd             make a plot of cross spectral density
draw            force a redraw of the current figure
errorbar        make an errorbar graph
figlegend       add a legend to the figure
figimage        add an image to the figure, w/o resampling
figtext         add text in figure coords
figure          create or change active figure
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
pcolor          make a pseudocolor plot
plotfile        plot data from a flat file
psd             make a plot of power spectral density
quiver          make a direction field (arrows) plot
rc              control the default params
savefig         save the current figure
scatter         make a scatter plot
setp            set a graphics property
semilogx        log x axis
semilogy        log y axis
show            show the figures
specgram        a spectrogram plot
stem            make a stem plot
subplot         make a subplot (numrows, numcols, axesnum)
table           add a table to the axes
=============== =========================================================



pylab functions
================i



pylab.hypergeometric           pylab.nan_to_num               pylab.select
pylab.hypot                    pylab.nbytes                   pylab.semilogx
pylab.add                      pylab.i0                       pylab.ndarray                  pylab.semilogy
pylab.add_docstring            pylab.identity                 pylab.ndenumerate              pylab.__setattr__
pylab.add_newdoc               pylab.diag                     pylab.ifft                     pylab.ndim                     pylab.setbufsize
pylab.add_newdocs              pylab.diagflat                 pylab.ifft2                    pylab.ndindex                  pylab.set_cmap
pylab.alen                     pylab.diagonal                 pylab.ifftn                    pylab.negative                 pylab.setdiff1d
pylab.all                      pylab.__dict__                 pylab.ifftshift                pylab.negative_binomial        pylab.seterr
pylab.allclose                 pylab.diff                     pylab.ihfft                    pylab.__new__                  pylab.seterrcall
pylab.ALLOW_THREADS            pylab.digitize                 pylab.iinfo                    pylab.newaxis                  pylab.seterrobj
pylab.alltrue                  pylab.disconnect               pylab.imag                     pylab.newbuffer                pylab.setmember1d
pylab.alterdot                 pylab.disp                     pylab.imread                   pylab.new_figure_manager       pylab.set_numeric_ops
pylab.amap                     pylab.dist                     pylab.imsave                   pylab.NINF                     pylab.setp
pylab.amax                     pylab.distances_along_curve    pylab.imshow                   pylab.noncentral_chisquare     pylab.set_printoptions
pylab.amin                     pylab.dist_point_to_segment    pylab.IndexDateFormatter       pylab.noncentral_f             pylab.set_state
pylab.angle                    pylab.divide                   pylab.index_exp                pylab.nonzero                  pylab.set_string_function
pylab.annotate                 pylab.__doc__                  pylab.IndexLocator             pylab.norm                     pylab.setxor1d
pylab.Annotation               pylab.dot                      pylab.indices                  pylab.normal                   pylab.shape
pylab.any                      pylab.double                   pylab.inexact                  pylab.normalize                pylab.SHIFT_DIVIDEBYZERO
pylab.append                   pylab.drange                   pylab.inf                      pylab.Normalize                pylab.SHIFT_INVALID
pylab.apply_along_axis         pylab.draw                     pylab.Inf                      pylab.norm_flat                pylab.SHIFT_OVERFLOW
pylab.apply_over_axes          pylab.draw_if_interactive      pylab.Infinity                 pylab.normpdf                  pylab.SHIFT_UNDERFLOW
pylab.arange                   pylab.dsplit                   pylab.info                     pylab.not_equal                pylab.short
pylab.arccos                   pylab.dstack                   pylab.infty                    pylab.np                       pylab.show
pylab.arccosh                  pylab.dtype                    pylab.__init__                 pylab.nper                     pylab.show_config
pylab.arcsin                   pylab.e                        pylab.inner                    pylab.npv                      pylab.shuffle
pylab.arcsinh                  pylab.ediff1d                  pylab.insert                   pylab.NullFormatter            pylab.sign
pylab.arctan                   pylab.eig                      pylab.inside_poly              pylab.NullLocator              pylab.signbit
pylab.arctan2                  pylab.eigh                     pylab.int_                     pylab.num2date                 pylab.signedinteger
pylab.arctanh                  pylab.eigvals                  pylab.int0                     pylab.num2epoch                pylab.silent_list
pylab.argmax                   pylab.eigvalsh                 pylab.int16                    pylab.number                   pylab.sin
pylab.argmin                   pylab.emath                    pylab.int32                    pylab.NZERO                    pylab.sinc
pylab.argsort                  pylab.empty                    pylab.int64                    pylab.obj2sctype               pylab.single
pylab.argwhere                 pylab.empty_like               pylab.int8                     pylab.object_                  pylab.singlecomplex
pylab.around                   pylab.entropy                  pylab.int_asbuffer             pylab.object0                  pylab.sinh
pylab.array                    pylab.epoch2num                pylab.intc                     pylab.ogrid                    pylab.size
pylab.array2string             pylab.equal                    pylab.integer                  pylab.ones                     pylab.Slider
pylab.array_equal              pylab.ERR_CALL                 pylab.interactive              pylab.ones_like                pylab.slopes
pylab.array_equiv              pylab.ERR_DEFAULT              pylab.interp                   pylab.outer                    pylab.solve
pylab.array_repr               pylab.ERR_DEFAULT2             pylab.intersect1d              pylab.over                     pylab.sometrue
pylab.array_split              pylab.ERR_IGNORE               pylab.intersect1d_nu           pylab.PackageLoader            pylab.sort
pylab.array_str                pylab.ERR_LOG                  pylab.intp                     pylab.packbits                 pylab.sort_complex
pylab.arrow                    pylab.errorbar                 pylab.inv                      pylab.pareto                   pylab.source
pylab.Arrow                    pylab.ERR_PRINT                pylab.invert                   pylab.path_length              pylab.specgram
pylab.Artist                   pylab.ERR_RAISE                pylab.ioff                     pylab.pcolor                   pylab.spectral
pylab.asanyarray               pylab.errstate                 pylab.ion                      pylab.pcolormesh               pylab.split
pylab.asarray                  pylab.ERR_WARN                 pylab.ipmt                     pylab.permutation              pylab.spring
pylab.asarray_chkfinite        pylab.exception_to_str         pylab.irefft                   pylab.pi                       pylab.spy
pylab.ascontiguousarray        pylab.exp                      pylab.irefft2                  pylab.sqrt
pylab.asfarray                 pylab.expand_dims              pylab.irefftn                  pylab.piecewise                pylab.square
pylab.asfortranarray           pylab.expm1                    pylab.irfft                    pylab.PINF                     pylab.squeeze
pylab.asmatrix                 pylab.exponential              pylab.irfft2                   pylab.pink                     pylab.standard_cauchy
pylab.asscalar                 pylab.exp_safe                 pylab.irfftn                   pylab.pinv                     pylab.standard_exponential
pylab.atleast_1d               pylab.extract                  pylab.irr                      pylab.pkgload                  pylab.standard_gamma
pylab.atleast_2d               pylab.eye                      pylab.is_closed_polygon        pylab.place                    pylab.standard_normal
pylab.atleast_3d               pylab.f                        pylab.iscomplex                pylab.plot                     pylab.standard_t
pylab.AutoLocator              pylab.fabs                     pylab.iscomplexobj             pylab.plot_date                pylab.std
pylab.autumn                   pylab.False_                   pylab.isfinite                 pylab.plotfile                 pylab.stem
acorr                    b.average                  pylab.fastCopyAndTranspose     pylab.isfortran                pylab.plotting                 pylab.step
pylab.axes                     pylab.fft                      pylab.ishold                   pylab.plt                      pylab.stineman_interp
pylab.Axes                     pylab.fft2                     pylab.isinf                    pylab.pmt                      pylab.__str__
pylab.axhline                  pylab.fftfreq                  pylab.isinteractive            pylab.poisson                  pylab.str_
pylab.axhspan                  pylab.fftn                     pylab.isnan                    pylab.polar                    pylab.string_
pylab.axis                     pylab.fftpack                  pylab.isneginf                 pylab.PolarAxes                pylab.string0
pylab.axvline                  pylab.fftpack_lite             pylab.is_numlike               pylab.poly                     pylab.strpdate2num
pylab.axvspan                  pylab.fftshift                 pylab.isposinf                 pylab.poly1d                   pylab.SU
pylab.bar                      pylab.fftsurr                  pylab.ispower2                 pylab.polyadd                  pylab.subplot
pylab.barbs                    pylab.figaspect                pylab.isreal                   pylab.poly_below               pylab.subplots_adjust
pylab.barh                     pylab.figimage                 pylab.isrealobj                pylab.poly_between             pylab.subplot_tool
pylab.bartlett                 pylab.figlegend                pylab.isscalar                 pylab.polyder                  pylab.SubplotTool
pylab.base_repr                pylab.fignum_exists            pylab.issctype                 pylab.polydiv                  pylab.subtract
pylab.bench                    pylab.figtext                  pylab.is_string_like           pylab.polyfit                  pylab.sum
pylab.beta                     pylab.figure                   pylab.issubclass_              pylab.Polygon                  pylab.summer
pylab.binary_repr              pylab.Figure                   pylab.issubdtype               pylab.polyint                  pylab.suptitle
pylab.bincount                 pylab.FigureCanvasBase         pylab.issubsctype              pylab.polymul                  pylab.svd
pylab.binomial                 pylab.__file__                 pylab.isvector                 pylab.polysub                  pylab.swapaxes
pylab.bitwise_and              pylab.fill                     pylab.iterable                 pylab.polyval                  pylab.switch_backend
pylab.bitwise_not              pylab.fill_between             pylab.ix_                      pylab.power                    pylab.sys
pylab.bitwise_or               pylab.fill_betweenx            pylab.jet                      pylab.ppmt                     pylab.table
pylab.bitwise_xor              pylab.find                     pylab.kaiser                   pylab.prctile                  pylab.take
pylab.bivariate_normal         pylab.find_common_type         pylab.kron                     pylab.prctile_rank             pylab.tan
pylab.blackman                 pylab.findobj                  pylab.l1norm                   pylab.prepca                   pylab.tanh
pylab.bmat                     pylab.finfo                    pylab.l2norm                   pylab.prism                    pylab.tensordot
pylab.bone                     pylab.fix                      pylab.lapack_lite              pylab.prod                     pylab.tensorinv
pylab.bool_                    pylab.FixedFormatter           pylab.laplace                  pylab.product                  pylab.tensorsolve
pylab.bool8                    pylab.FixedLocator             pylab.ldexp                    pylab.psd                      pylab.test
pylab.box                      pylab.flag                     pylab.left_shift               pylab.ptp                      pylab.Tester
pylab.boxplot                  pylab.flatiter                 pylab.legend                   pylab.put                      pylab.text
pylab.broadcast                pylab.flatnonzero              pylab.less                     pylab.putmask                  pylab.Text
pylab.broadcast_arrays         pylab.flatten                  pylab.less_equal               pylab.pv                       pylab.TH
pylab.broken_barh              pylab.flexible                 pylab.levypdf                  pylab.pylab_setup              pylab.thetagrids
pylab.BUFSIZE                  pylab.fliplr                   pylab.lexsort                  pylab.PZERO                    pylab.TickHelper
pylab.__builtins__             pylab.flipud                   pylab.liaupunov                pylab.qr                       pylab.tile
pylab.Button                   pylab.float_                   pylab.linalg                   pylab.quiver                   pylab.title
pylab.byte                     pylab.float32                  pylab.LinAlgError              pylab.quiverkey                pylab.trace
pylab.byte_bounds              pylab.float64                  pylab.r_                       pylab.transpose
pylab.bytes                    pylab.float96                  pylab.LinearLocator            pylab.radians                  pylab.trapz
pylab.c_                       pylab.floating                 pylab.linspace                 pylab.RAISE                    pylab.tri
pylab.can_cast                 pylab.FLOATING_POINT_SUPPORT   pylab.little_endian            pylab.rand                     pylab.triangular
pylab.cast                     pylab.floor                    pylab.load                     pylab.randint                  pylab.tril
pylab.cbook                    pylab.floor_divide             pylab.loads                    pylab.randn                    pylab.trim_zeros
pylab.cdouble                  pylab.fmod                     pylab.loadtxt                  pylab.triu
pylab.ceil                     pylab.format_parser            pylab.Locator                  pylab.random_integers          pylab.True_
pylab.center_matrix            pylab.FormatStrFormatter       pylab.log                      pylab.random_sample            pylab.true_divide
pylab.cfloat                   pylab.Formatter                pylab.log10                    pylab.ranf                     pylab.TU
pylab.char                     pylab.FPE_DIVIDEBYZERO         pylab.log1p                    pylab.rank                     pylab.twinx
pylab.character                pylab.FPE_INVALID              pylab.log2                     pylab.RankWarning              pylab.twiny
pylab.chararray                pylab.FPE_OVERFLOW             pylab.LogFormatter             pylab.rate                     pylab.typecodes
pylab.chisquare                pylab.FPE_UNDERFLOW            pylab.LogFormatterExponent     pylab.ravel                    pylab.typeDict
pylab.cholesky                 pylab.FR                       pylab.LogFormatterMathtext     pylab.rayleigh                 pylab.typeNA
pylab.choose                   pylab.frange                   pylab.logical_and              pylab.rc                       pylab.typename
pylab.Circle                   pylab.frexp                    pylab.logical_not              pylab.rcdefaults               pylab.ubyte
pylab.cla                      pylab.frombuffer               pylab.logical_or               pylab.rcParams                 pylab.ufunc
pylab.clabel                   pylab.fromfile                 pylab.logical_xor              pylab.rcParamsDefault          pylab.UFUNC_BUFSIZE_DEFAULT
pylab.__class__                pylab.fromfunction             pylab.logistic                 pylab.real                     pylab.UFUNC_PYVALS_NAME
pylab.clf                      pylab.fromiter                 pylab.LogLocator               pylab.real_if_close            pylab.uint
pylab.clim                     pylab.frompyfunc               pylab.rec                      pylab.uint0
pylab.clip                     pylab.fromregex                pylab.lognormal                pylab.rec2csv                  pylab.uint16
pylab.CLIP                     pylab.fromstring               pylab.logseries                pylab.rec_append_fields        pylab.uint32
pylab.clongdouble              pylab.FuncFormatter            pylab.logspace                 pylab.recarray                 pylab.uint64
pylab.clongfloat               pylab.fv                       pylab.longcomplex              pylab.rec_drop_fields          pylab.uint8
pylab.close                    pylab.gamma                    pylab.longdouble               pylab.reciprocal               pylab.uintc
pylab.cm                       pylab.gca                      pylab.longest_contiguous_ones  pylab.rec_join                 pylab.uintp
pylab.cohere                   pylab.gcf                      pylab.longest_ones             pylab.record                   pylab.ulonglong
pylab.colorbar                 pylab.gci                      pylab.longfloat                pylab.Rectangle                pylab.unicode_
pylab.colormaps                pylab.generic                  pylab.longlong                 pylab.__reduce__               pylab.unicode0
pylab.colors                   pylab.geometric                pylab.lookfor                  pylab.__reduce_ex__            pylab.uniform
pylab.column_stack             pylab.get                      pylab.lstsq                    pylab.refft                    pylab.union1d
pylab.common_type              pylab.get_array_wrap           pylab.ma                       pylab.refft2                   pylab.unique
pylab.compare_chararrays       pylab.__getattribute__         pylab.MachAr                   pylab.refftn                   pylab.unique1d
pylab.complex_                 pylab.get_backend              pylab.mat                      pylab.register_cmap            pylab.unpackbits
pylab.complex128               pylab.getbuffer                pylab.math                     pylab.relativedelta            pylab.unravel_index
pylab.complex192               pylab.getbufsize               pylab.matplotlib               pylab.remainder                pylab.unsignedinteger
pylab.complex64                pylab.get_cmap                 pylab.matrix                   pylab.repeat                   pylab.unwrap
pylab.complexfloating          pylab.get_current_fig_manager  pylab.matrix_power             pylab.__repr__                 pylab.ushort
pylab.compress                 pylab.geterr                   pylab.matshow                  pylab.require                  pylab.vander
pylab.concatenate              pylab.geterrcall               pylab.MAXDIMS                  pylab.reshape                  pylab.var
pylab.cond                     pylab.geterrobj                pylab.maximum                  pylab.resize                   pylab.vdot
pylab.conj                     pylab.get_fignums              pylab.maximum_sctype           pylab.restoredot               pylab.vectorize
pylab.conjugate                pylab.get_include              pylab.MaxNLocator              pylab.rfft                     pylab.vector_lengths
pylab.connect                  pylab.get_numarray_include     pylab.may_share_memory         pylab.rfft2                    pylab.vlines
pylab.contour                  pylab.get_numpy_include        pylab.mean                     pylab.rfftn                    pylab.void
pylab.contourf                 pylab.getp                     pylab.median                   pylab.rgrids                   pylab.void0
pylab.convolve                 pylab.get_plot_commands        pylab.memmap                   pylab.right_shift              pylab.vonmises
pylab.cool                     pylab.get_printoptions         pylab.meshgrid                 pylab.rint                     pylab.vsplit
pylab.copper                   pylab.get_scale_docs           pylab.mgrid                    pylab.rk4                      pylab.vstack
pylab.copy                     pylab.get_scale_names          pylab.minimum                  pylab.rms_flat                 pylab.waitforbuttonpress
pylab.corrcoef                 pylab.get_sparse_matrix        pylab.minorticks_off           pylab.roll                     pylab.wald
pylab.correlate                pylab.get_state                pylab.minorticks_on            pylab.rollaxis                 pylab.warnings
pylab.cos                      pylab.get_xyz_where            pylab.mintypecode              pylab.roots                    pylab.WE
pylab.cosh                     pylab.ginput                   pylab.MinuteLocator            pylab.rot90                    pylab.WeekdayLocator
pylab.cov                      pylab.gradient                 pylab.MINUTELY                 pylab.round_                   pylab.WEEKLY
pylab.cross                    pylab.gray                     pylab.mirr                     pylab.row_stack                pylab.weibull
pylab.csd                      pylab.greater                  pylab.mlab                     pylab.rrule                    pylab.where
pylab.csingle                  pylab.greater_equal            pylab.MO                       pylab.RRuleLocator             pylab.who
pylab.csv2rec                  pylab.grid                     pylab.mod                      pylab.s_                       pylab.Widget
pylab.ctypeslib                pylab.griddata                 pylab.modf                     pylab.SA                       pylab.window_hanning
pylab.cumprod                  pylab.gumbel                   pylab.MonthLocator             pylab.safe_eval                pylab.window_none
pylab.cumproduct               pylab.hamming                  pylab.MONTHLY                  pylab.sample                   pylab.winter
pylab.cumsum                   pylab.hanning                  pylab.movavg                   pylab.save                     pylab.WRAP
pylab.DAILY                    pylab.__hash__                 pylab.mpl                      pylab.savefig                  pylab.xcorr
pylab.DataSource               pylab.helper                   pylab.msort                    pylab.savetxt                  pylab.xlabel
pylab.date2num                 pylab.hexbin                   pylab.multinomial              pylab.savez                    pylab.xlim
pylab.DateFormatter            pylab.hfft                     pylab.MultipleLocator          pylab.ScalarFormatter          pylab.xscale
pylab.DateLocator              pylab.hist                     pylab.multiply                 pylab.ScalarType               pylab.xticks
pylab.datestr2num              pylab.histogram                pylab.multivariate_normal      pylab.scatter                  pylab.YearLocator
pylab.DayLocator               pylab.histogram2d              pylab.mx2num                   pylab.sci                      pylab.YEARLY
pylab.dedent                   pylab.histogramdd              pylab.__name__                 pylab.sctype2char              pylab.ylabel
pylab.degrees                  pylab.hlines                   pylab.nan                      pylab.sctypeDict               pylab.ylim
pylab.__delattr__              pylab.hold                     pylab.NaN                      pylab.sctypeNA                 pylab.yscale
pylab.delaxes                  pylab.hot                      pylab.NAN                      pylab.sctypes                  pylab.yticks
pylab.delete                   pylab.HourLocator              pylab.nanargmax                pylab.searchsorted             pylab.zeros
pylab.demean                   pylab.HOURLY                   pylab.nanargmin                pylab.SecondLocator            pylab.zeros_like
pylab.deprecate                pylab.hsplit                   pylab.nanmax                   pylab.SECONDLY                 pylab.zipf
pylab.deprecate_with_doc       pylab.hstack                   pylab.nanmin                   pylab.seed                     
pylab.det                      pylab.hsv                      pylab.nansum                   pylab.segments_intersec






pylab.matplotlib.afm                     pylab.matplotlib.distutils               pylab.matplotlib._mathtext_data          pylab.matplotlib.__reduce__
pylab.matplotlib.artist                  pylab.matplotlib.__doc__                 pylab.matplotlib.matplotlib_fname        pylab.matplotlib.__reduce_ex__
pylab.matplotlib.axes                    pylab.matplotlib.figure                  pylab.matplotlib.minor1                  pylab.matplotlib.__repr__
pylab.matplotlib.axis                    pylab.matplotlib.__file__                pylab.matplotlib.minor2                  pylab.matplotlib.__revision__
pylab.matplotlib.backend_bases           pylab.matplotlib.finance                 pylab.matplotlib.mlab                    pylab.matplotlib.s
pylab.matplotlib.backends                pylab.matplotlib.fontconfig_pattern      pylab.matplotlib.mpl                     pylab.matplotlib.scale
pylab.matplotlib.bezier                  pylab.matplotlib.font_manager            pylab.matplotlib.__name__                pylab.matplotlib.__setattr__
pylab.matplotlib.blocking_input          pylab.matplotlib.ft2font                 pylab.matplotlib.__new__                 pylab.matplotlib.shutil
pylab.matplotlib.__builtins__            pylab.matplotlib.generators              pylab.matplotlib.NEWCONFIG               pylab.matplotlib.spines
pylab.matplotlib.cbook                   pylab.matplotlib.__getattribute__        pylab.matplotlib.nn                      pylab.matplotlib.__str__
pylab.matplotlib.checkdep_dvipng         pylab.matplotlib.get_backend             pylab.matplotlib.numpy                   pylab.matplotlib.subprocess
pylab.matplotlib.checkdep_ghostscript    pylab.matplotlib._get_configdir          pylab.matplotlib.nxutils                 pylab.matplotlib.sys
pylab.matplotlib.checkdep_pdftops        pylab.matplotlib.get_configdir           pylab.matplotlib.offsetbox               pylab.matplotlib.table
pylab.matplotlib.checkdep_ps_distiller   pylab.matplotlib._get_data_path          pylab.matplotlib.os                      pylab.matplotlib.tempfile
pylab.matplotlib.checkdep_tex            pylab.matplotlib.get_data_path           pylab.matplotlib.patches                 pylab.matplotlib.text
pylab.matplotlib.checkdep_usetex         pylab.matplotlib._get_data_path_cached   pylab.matplotlib.path                    pylab.matplotlib.ticker
pylab.matplotlib.__class__               pylab.matplotlib.get_example_data        pylab.matplotlib._path                   pylab.matplotlib.tight_bbox
pylab.matplotlib.cm                      pylab.matplotlib._get_home               pylab.matplotlib.__path__                pylab.matplotlib.tk_window_focus
pylab.matplotlib._cm                     pylab.matplotlib.get_home                pylab.matplotlib._png                    pylab.matplotlib.tmp
pylab.matplotlib._cntr                   pylab.matplotlib.get_py2exe_datafiles    pylab.matplotlib.projections             pylab.matplotlib.transforms
pylab.matplotlib.collections             pylab.matplotlib.__hash__                pylab.matplotlib.pylab                   pylab.matplotlib.units
pylab.matplotlib.colorbar                pylab.matplotlib._havedate               pylab.matplotlib._pylab_helpers          pylab.matplotlib.use
pylab.matplotlib.colors                  pylab.matplotlib.image                   pylab.matplotlib.pyparsing               pylab.matplotlib._use_error_msg
pylab.matplotlib.compare_versions        pylab.matplotlib._image                  pylab.matplotlib.pyplot                  pylab.matplotlib.validate_backend
pylab.matplotlib.contour                 pylab.matplotlib.__init__                pylab.matplotlib._python24               pylab.matplotlib.validate_cairo_format
pylab.matplotlib.converter               pylab.matplotlib.interactive             pylab.matplotlib.quiver                  pylab.matplotlib.validate_toolbar
pylab.matplotlib.__date__                pylab.matplotlib.is_interactive          pylab.matplotlib.rc                      pylab.matplotlib.verbose
pylab.matplotlib.dates                   pylab.matplotlib.is_string_like          pylab.matplotlib.rcdefaults              pylab.matplotlib.Verbose
pylab.matplotlib.default                 pylab.matplotlib._is_writable_dir        pylab.matplotlib.rc_params               pylab.matplotlib.__version__
pylab.matplotlib.defaultParams           pylab.matplotlib.key                     pylab.matplotlib.rcParams                pylab.matplotlib.warnings
pylab.matplotlib.__delattr__             pylab.matplotlib.legend                  pylab.matplotlib.RcParams                pylab.matplotlib.widgets
pylab.matplotlib._deprecated_ignore_map  pylab.matplotlib.lines                   pylab.matplotlib.rcParamsDefault         
pylab.matplotlib._deprecated_map         pylab.matplotlib.major                   pylab.matplotlib.rcsetup                 
pylab.matplotlib.__dict__                pylab.matplotlib.mathtext                pylab.matplotlib.re         








pylab.matplotlib.mlab.amap                              pylab.matplotlib.mlab.FormatDate                        pylab.matplotlib.mlab.np
pylab.matplotlib.mlab.base_repr                         pylab.matplotlib.mlab.FormatDatetime                    pylab.matplotlib.mlab.nxutils
pylab.matplotlib.mlab.binary_repr                       pylab.matplotlib.mlab.FormatFloat                       pylab.matplotlib.mlab.operator
pylab.matplotlib.mlab.bivariate_normal                  pylab.matplotlib.mlab.FormatFormatStr                   pylab.matplotlib.mlab.os
pylab.matplotlib.mlab.__builtins__                      pylab.matplotlib.mlab.FormatInt                         pylab.matplotlib.mlab.path_length
pylab.matplotlib.mlab.cbook                             pylab.matplotlib.mlab.FormatMillions                    pylab.matplotlib.mlab.poly_below
pylab.matplotlib.mlab.center_matrix                     pylab.matplotlib.mlab.FormatObj                         pylab.matplotlib.mlab.poly_between
pylab.matplotlib.mlab.__class__                         pylab.matplotlib.mlab.FormatPercent                     pylab.matplotlib.mlab.prctile
pylab.matplotlib.mlab.cohere                            pylab.matplotlib.mlab.FormatString                      pylab.matplotlib.mlab.prctile_rank
pylab.matplotlib.mlab.cohere_pairs                      pylab.matplotlib.mlab.FormatThousands                   pylab.matplotlib.mlab.prepca
pylab.matplotlib.mlab._coh_error                        pylab.matplotlib.mlab.frange                            pylab.matplotlib.mlab.psd
pylab.matplotlib.mlab.contiguous_regions                pylab.matplotlib.mlab.__getattribute__                  pylab.matplotlib.mlab.quad2cubic
pylab.matplotlib.mlab.copy                              pylab.matplotlib.mlab.get_formatd                       pylab.matplotlib.mlab.rec2csv
pylab.matplotlib.mlab.cross_from_above                  pylab.matplotlib.mlab.get_sparse_matrix                 pylab.matplotlib.mlab.rec2txt
pylab.matplotlib.mlab.cross_from_below                  pylab.matplotlib.mlab.get_xyz_where                     pylab.matplotlib.mlab.rec_append_fields
pylab.matplotlib.mlab.csd                               pylab.matplotlib.mlab.griddata                          pylab.matplotlib.mlab.rec_drop_fields
pylab.matplotlib.mlab.csv                               pylab.matplotlib.mlab.__hash__                          pylab.matplotlib.mlab.rec_groupby
pylab.matplotlib.mlab.csv2rec                           pylab.matplotlib.mlab.identity                          pylab.matplotlib.mlab.rec_join
pylab.matplotlib.mlab.csvformat_factory                 pylab.matplotlib.mlab.__init__                          pylab.matplotlib.mlab.rec_keep_fields
pylab.matplotlib.mlab.defaultformatd                    pylab.matplotlib.mlab.inside_poly                       pylab.matplotlib.mlab.rec_summarize
pylab.matplotlib.mlab.__delattr__                       pylab.matplotlib.mlab.is_closed_polygon                 pylab.matplotlib.mlab.__reduce__
pylab.matplotlib.mlab.demean                            pylab.matplotlib.mlab.ispower2                          pylab.matplotlib.mlab.__reduce_ex__
pylab.matplotlib.mlab.isvector                          pylab.matplotlib.mlab.__repr__
pylab.matplotlib.mlab.kwdocd                            pylab.matplotlib.mlab.rk4
pylab.matplotlib.mlab.l1norm                            pylab.matplotlib.mlab.rms_flat
pylab.matplotlib.mlab.l2norm                            pylab.matplotlib.mlab.safe_isinf
pylab.matplotlib.mlab.__dict__                          pylab.matplotlib.mlab.less_simple_linear_interpolation  pylab.matplotlib.mlab.safe_isnan
pylab.matplotlib.mlab.dist                              pylab.matplotlib.mlab.levypdf                           pylab.matplotlib.mlab.save
pylab.matplotlib.mlab.distances_along_curve             pylab.matplotlib.mlab.liaupunov                         pylab.matplotlib.mlab.segments_intersect
pylab.matplotlib.mlab.dist_point_to_segment             pylab.matplotlib.mlab.load                              pylab.matplotlib.mlab.__setattr__
pylab.matplotlib.mlab.division                          pylab.matplotlib.mlab.log2                              pylab.matplotlib.mlab.slopes
pylab.matplotlib.mlab.__doc__                           pylab.matplotlib.mlab.logspace                          pylab.matplotlib.mlab.specgram
pylab.matplotlib.mlab.donothing_callback                pylab.matplotlib.mlab.longest_contiguous_ones           pylab.matplotlib.mlab._spectral_helper
pylab.matplotlib.mlab.entropy                           pylab.matplotlib.mlab.longest_ones                      pylab.matplotlib.mlab.stineman_interp
pylab.matplotlib.mlab.exp_safe                          pylab.matplotlib.mlab.ma                                pylab.matplotlib.mlab.__str__
pylab.matplotlib.mlab.exp_safe_MAX                      pylab.matplotlib.mlab.math                              pylab.matplotlib.mlab.vector_lengths
pylab.matplotlib.mlab.exp_safe_MIN                      pylab.matplotlib.mlab.movavg                            pylab.matplotlib.mlab.verbose
pylab.matplotlib.mlab.fftsurr                           pylab.matplotlib.mlab.__name__                          pylab.matplotlib.mlab.warnings
pylab.matplotlib.mlab.FIFOBuffer                        pylab.matplotlib.mlab.__new__                           pylab.matplotlib.mlab.window_hanning
pylab.matplotlib.mlab.__file__                          pylab.matplotlib.mlab._norm                             pylab.matplotlib.mlab.window_none
pylab.matplotlib.mlab.find                              pylab.matplotlib.mlab.norm_flat                         
pylab.matplotlib.mlab.FormatBool                        pylab.matplotlib.mlab.normpdf   


matplotlib.afm                     matplotlib.dates                   matplotlib.__hash__                matplotlib.os                      matplotlib.__setattr__
matplotlib.artist                  matplotlib.default                 matplotlib._havedate               matplotlib.patches                 matplotlib.shutil
matplotlib.axes                    matplotlib.defaultParams           matplotlib.image                   matplotlib.path                    matplotlib.spines
matplotlib.axis                    matplotlib.__delattr__             matplotlib._image                  matplotlib._path                   matplotlib.__str__
matplotlib.backend_bases           matplotlib._deprecated_ignore_map  matplotlib.__init__                matplotlib.__path__                matplotlib.subprocess
matplotlib.backends                matplotlib._deprecated_map         matplotlib.interactive             matplotlib._png                    matplotlib.sys
matplotlib.bezier                  matplotlib.__dict__                matplotlib.is_interactive          matplotlib.projections             matplotlib.table
matplotlib.blocking_input          matplotlib.distutils               matplotlib.is_string_like          matplotlib.pylab                   matplotlib.tempfile
matplotlib.__builtins__            matplotlib.__doc__                 matplotlib._is_writable_dir        matplotlib._pylab_helpers          matplotlib.text
matplotlib.cbook                   matplotlib.figure                  matplotlib.key                     matplotlib.pyparsing               matplotlib.ticker
matplotlib.checkdep_dvipng         matplotlib.__file__                matplotlib.legend                  matplotlib.pyplot                  matplotlib.tight_bbox
matplotlib.checkdep_ghostscript    matplotlib.finance                 matplotlib.lines                   matplotlib._python24               matplotlib.tk_window_focus
matplotlib.checkdep_pdftops        matplotlib.fontconfig_pattern      matplotlib.major                   matplotlib.quiver                  matplotlib.tmp
matplotlib.checkdep_ps_distiller   matplotlib.font_manager            matplotlib.mathtext                matplotlib.rc                      matplotlib.transforms
matplotlib.checkdep_tex            matplotlib.ft2font                 matplotlib._mathtext_data          matplotlib.rcdefaults              matplotlib.units
matplotlib.checkdep_usetex         matplotlib.generators              matplotlib.matplotlib_fname        matplotlib.rc_params               matplotlib.use
matplotlib.__class__               matplotlib.__getattribute__        matplotlib.minor1                  matplotlib.rcParams                matplotlib._use_error_msg
matplotlib.cm                      matplotlib.get_backend             matplotlib.minor2                  matplotlib.RcParams                matplotlib.validate_backend
matplotlib._cm                     matplotlib._get_configdir          matplotlib.mlab                    matplotlib.rcParamsDefault         matplotlib.validate_cairo_format
matplotlib._cntr                   matplotlib.get_configdir           matplotlib.mpl                     matplotlib.rcsetup                 matplotlib.validate_toolbar
matplotlib.collections             matplotlib._get_data_path          matplotlib.__name__                matplotlib.re                      matplotlib.verbose
matplotlib.get_data_path           matplotlib.__new__                 matplotlib.__reduce__              matplotlib.Verbose
matplotlib._get_data_path_cached   matplotlib.NEWCONFIG               matplotlib.__reduce_ex__           matplotlib.__version__
matplotlib.compare_versions        matplotlib.get_example_data        matplotlib.nn                      matplotlib.__repr__                matplotlib.warnings
matplotlib.contour                 matplotlib._get_home               matplotlib.numpy                   matplotlib.__revision__            matplotlib.widgets
matplotlib.converter               matplotlib.get_home                matplotlib.nxutils                 matplotlib.s                       
matplotlib.__date__                matplotlib.get_py2exe_datafiles    matplotlib.offsetbox               matplotlib.scale                






 cumsum    - the cumulative sum along a dimension
      diag      - the k-th diagonal of matrix
      diff      - the n-th differnce of an array
      eig       - the eigenvalues and eigen vectors of v
      eye       - a matrix where the k-th diagonal is ones, else zero
      find      - return the indices where a condition is nonzero
      fliplr    - flip the rows of a matrix up/down
      flipud    - flip the columns of a matrix left/right
      linspace  - a linear spaced vector of N values from min to max inclusive
      logspace  - a log spaced vector of N values from min to max inclusive
      meshgrid  - repeat x and y to make regular matrices
      ones      - an array of ones
      rand      - an array from the uniform distribution [0,1]
      randn     - an array from the normal distribution
      rot90     - rotate matrix k*90 degress counterclockwise
      squeeze   - squeeze an array removing any dimensions of length 1
      tri       - a triangular matrix
      tril      - a lower triangular matrix
      triu      - an upper triangular matrix
      vander    - the Vandermonde matrix of vector x
      svd       - singular value decomposition
      zeros     - a matrix of zeros

   _Probability
    
      levypdf   - The levy probability density function from the char. func.
      normpdf   - The Gaussian probability density function
      rand      - random numbers from the uniform distribution
      randn     - random numbers from the normal distribution
    
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
    
      bartlett  - M-point Bartlett window
      blackman  - M-point Blackman window
      cohere    - the coherence using average periodiogram
      csd       - the cross spectral density using average periodiogram
      fft       - the fast Fourier transform of vector x
      hamming   - M-point Hamming window
      hanning   - M-point Hanning window
      hist      - compute the histogram of x
      kaiser    - M length Kaiser window
      psd       - the power spectral density using average periodiogram
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




