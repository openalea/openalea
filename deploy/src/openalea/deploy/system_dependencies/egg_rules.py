# -*- python -*-
#
#       openalea.deploy.dependency_builder
#
#       Copyright 2006-2012 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau
#       File Contributors(s):   
#                             - Yassin Refahi,
#                             - Frederic Boudon,
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

################################################################################
# - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - EGG BUILDERS - #
# !!!!   THE ORDER OF CLASS DEFINITIONS IS THE ORDER OF EGG COMPILATION    !!!!#
################################################################################        
class egg_mingw_rt(BaseEggBuilder):
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Development (compiler, linker, libs, includes)"
    py_dependent   = False
    arch_dependent = True
    version        = "5.1.4_4b"
    def script_substitutions(self):
        mgw = mingwrt()
        libdirs = {"bin":mgw.install_dll_dir}
        return dict( 
                    VERSION  = self.version,
                    LIB_DIRS = libdirs,
                    )                

class egg_mingw(BaseEggBuilder):
    license = "PublicDomain for MingW runtime. GLP or LGPL for some libraries."
    authors = "The Mingw Project"
    description = "Mingw Runtime"
    py_dependent   = False
    arch_dependent = True
    def script_substitutions(self):
        cpath = Compiler.get_bin_path()
        mingwbase = pj(cpath,os.pardir)
        subd  = os.listdir( mingwbase )
        subd.remove("EGG-INFO")
        subd.remove("bin")
        subd.remove("include")
        data = []
        
        for dir in subd:
            dat = recursive_glob_as_dict(pj(mingwbase,dir), "*", strip_keys=True, prefix_key=dir).items()         
            data += [ (d, [f for f in t if not f.endswith(".dll")]) for d,t in dat]

        bindirs = {"bin": cpath}
        incdirs = {"include": pj(mingwbase, "include")}
            
        return dict( 
                    VERSION  = egg_mingw_rt.version,
                    BIN_DIRS = bindirs,
                    INC_DIRS = incdirs,
                    DATA_FILES   = data,
                    )  
    
class egg_qt4(BaseEggBuilder):
    license = "General Public License V3"
    authors = "Riverbank Computing (Sip+PyQt4+QSCintilla) & Nokia (Qt4)"
    description = "Sip+PyQt4+QScintilla Runtime packaged as an egg for windows-gcc"
    py_dependent   = True
    arch_dependent = True
    def script_substitutions(self):        
        qt4_   = qt4()
        pyqt4_ = pyqt4()
        pysci_ = pyqscintilla()
        sip_   = sip()
        # dlls are the union of qt dlls and plugins directories (which is actually the same!)
        # qscis apis are recursive from qt4 (need to list all files)        
        qscis    = recursive_glob_as_dict(pysci_.qsci_dir, Pattern.sciapi, strip_keys=True, prefix_key="qsci").items()
        extra_pyqt4_mods = recursive_glob_as_dict(pj(pyqt4_.install_site_dir,"PyQt4"), Pattern.pyall, strip_keys=True, prefix_key="PyQt4").items()
        print "laaaaaaaaaaaaaaaajfdshfsdosfdo", extra_pyqt4_mods
        sip_mods = recursive_glob_as_dict(sip_.install_site_dir, Pattern.pyall, strip_keys=True, levels=1).items()

        lib_dirs    = {"PyQt4": qt4_.install_dll_dir}
        package_dir = {"PyQt4": pj(pyqt4_.install_site_dir, "PyQt4")}
        
        from openalea.vpltk.qt import QtCore
        from setuptools import find_packages
        return dict( 
                    VERSION  = QtCore.QT_VERSION_STR,
                    PACKAGES = find_packages(pyqt4_.install_site_dir, "PyQt4"),
                    PACKAGE_DIRS = package_dir,
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    
                    LIB_DIRS         = lib_dirs,
                    DATA_FILES       = qscis+sip_mods+extra_pyqt4_mods,
                    INSTALL_REQUIRES = [egg_mingw_rt.egg_name()]
                    )  
                    
class egg_qt4_dev(BaseEggBuilder):
    license = "General Public License V3"
    authors = "Riverbank Computing (Sip+PyQt4+QSCintilla) & Nokia (Qt4)"
    description = "Sip+PyQt4+QScintilla Development packaged as an egg for windows-gcc"
    py_dependent   = True
    arch_dependent = True
    def script_substitutions(self):
        qt4_   = qt4()
        pyqt4_ = pyqt4()
        sip_   = sip()
        # binaries are the union of qt, pyqt and sip binaries 
        bin_dirs = {"bin":qt4_.install_bin_dir}
        # includes are recursive subdirectories and the union of qt and sip includes               
        incs = recursive_glob_as_dict( qt4_.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items() + \
               recursive_glob_as_dict( sip_.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qt4_.install_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories and the union of pyqt4 and...
        sips = recursive_glob_as_dict(pyqt4_.install_sip_dir, Pattern.sipfiles, strip_keys=True, prefix_key="sip").items()
        # sources are recursive subdirectories and the union of qt4 and that all (CPP have been removed)...
        srcs = recursive_glob_as_dict(qt4_.install_src_dir, Pattern.qtsrc, strip_keys=True, prefix_key="src").items()
        # tra files are recursive subdirectories in qt4
        tra = recursive_glob_as_dict(qt4_.install_tra_dir, Pattern.qttransl, strip_keys=True, prefix_key="translations").items()
        # mks files are recursive subdirectories in qt4
        mks = recursive_glob_as_dict(qt4_.install_mks_dir, Pattern.qtmkspec, strip_keys=True, prefix_key="mkspecs").items()        
        # plugins files are recursive subdirectories in qt4
        plu = recursive_glob_as_dict(qt4_.install_plu_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="plugins").items()        

        from openalea.vpltk.qt import QtCore
        
        return dict( 
                    VERSION          = QtCore.QT_VERSION_STR,                   
                    BIN_DIRS         = bin_dirs,
                    INC_DIRS         = inc_dirs,
                    DATA_FILES       = libs+sips+srcs+tra+mks+plu,
                    INSTALL_REQUIRES = [egg_qt4.egg_name()]
                    )  
                    
class egg_pyqglviewer(BaseEggBuilder):
    license = "General Public License"
    authors = "libQGLViewer developers for libQGLViewer, PyQGLViewer (INRIA) developers for PyQGLViewer"
    description = "Win-GCC version of PyQGLViewer"
    py_dependent   = True
    arch_dependent = True
    def script_substitutions(self):
        qt4_   = qt4()
        qglv_   = qglviewer()
        pyqglv_   = pyqglviewer()
        
        pyqgl_mods = recursive_glob_as_dict(pyqglv_.install_site_dir, Pattern.pyall, strip_keys=True, levels=1).items()
        # includes are recursive subdirectories of qglviewer           
        incs = recursive_glob_as_dict( qglv_.install_inc_dir, Pattern.include, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
        # libs are recursive subdirectories of qt libs          
        libs = recursive_glob_as_dict(qglv_.install_lib_dir, Pattern.qtstalib, strip_keys=True, prefix_key="lib").items()
        # sip files are recursive subdirectories of pyqglviewer sip installation directory
        sips = recursive_glob_as_dict(pyqglv_.install_sip_dir, Pattern.sipfiles, strip_keys=True, prefix_key="sip").items()
        # examples are recursive subdirectories of pyqglviewer examples installation directory contains various types of files
        exas = recursive_glob_as_dict(pyqglv_.install_exa_dir, Pattern.any, strip_keys=True, prefix_key="examples").items()        
        
        lib_dirs    = {"" : qglv_.install_dll_dir}
        data_files  = exas+sips+libs+pyqgl_mods
        
        import PyQGLViewer
        
        return dict( 
                    VERSION      = PyQGLViewer.QGLViewerVersionString(),                                  
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    #PACKAGE_DIRS = package_dir,                    
                    LIB_DIRS     = lib_dirs,
                    INC_DIRS     = inc_dirs,
                    
                    DATA_FILES   = data_files,
                    INSTALL_REQUIRES = [egg_qt4.egg_name()]
                    )  
                    
class egg_boost(BaseEggBuilder):
    license = "Boost Software License 1.0"
    authors = "Boost contributors"
    description = "Windows gcc libs and includes of Boost"    
    py_dependent   = True
    arch_dependent = True    
    def script_substitutions(self):
        version_re  = re_compile("^.*BOOST_VERSION\s:\s([\d\.]{4,8}).*$", re.MULTILINE|re.DOTALL)
        boost_ = boost()
                  
        incs = recursive_glob_as_dict( boost_.install_inc_dir, Pattern.qtinc, strip_keys=True, prefix_key="include", dirs=True).items()
        inc_dirs = merge_list_dict( incs )
           
        # get the version from Jamroot file
        version = "UNKNOWN"        
        with open( pj(boost_.sourcedir, "Jamroot") ) as f:
            txt = f.read()
            se = version_re.search(txt)
            if se:
                version = se.groups()[0]
        lib_dirs    = {"lib": boost_.install_lib_dir}
        
        return dict( 
                    VERSION          = version,                 
                    LIB_DIRS         = lib_dirs,
                    INC_DIRS         = inc_dirs,
                    INSTALL_REQUIRES = [egg_mingw_rt.egg_name()]
                    )  

class egg_ann(BaseEggBuilder): 
    license = "GNU Lesser Public License"
    authors = "Copyright (c) 1997-2010 University of Maryland and Sunil Arya and David Mount"
    description = "Windows gcc libs and includes of ANN"
    py_dependent   = False
    arch_dependent = True  
    def script_substitutions(self):
        ann_ = ann()
        ann_path = ann_.sourcedir
        
        return dict( 
                    VERSION          = ann_.version,                 
                    LIB_DIRS         = {'lib' : pj(ann_path,'lib') },
                    INC_DIRS         = {'include' : pj(ann_path,'include') },
                    BIN_DIRS         = {'bin' : pj(ann_path,'bin') },
                    DATA_FILES       = [('doc' , [pj(ann_path,'doc','ANNmanual.pdf')] )]
                    ) 

class egg_cgal(BaseEggBuilder): 
    license = "GNU Lesser Public License"
    authors = "CGAL, Computational Geometry Algorithms Library, http://www.cgal.org"
    description = "Windows gcc libs and includes of CGAL"
    py_dependent   = False
    arch_dependent = True  
    def script_substitutions(self):
        cgal_ = cgal()
        cgal_path = cgal_.sourcedir
        
        return dict( 
                    VERSION          = cgal_.version,
                    URL              = "http://www.cgal.org",
                    LIB_DIRS         = {'lib' : pj(cgal_path,'lib') },
                    INC_DIRS         = {'include' : pj(cgal_path,'include') },
                    BIN_DIRS         = {'bin' : pj(cgal_path,'bin') },
                    #DATA_FILES       = [('doc' , glob.glob(pj(cgal_path,'doc_html','*')) )]
                    ) 

# class egg_gnuplot(BaseEggBuilder): 
    # license = "GNUPlot license"
    # authors = "Copyright 1986 - 1993, 1998, 2004 Thomas Williams, Colin Kelley"
    # description = "Windows gcc libs and includes of gnuplot"
    # py_dependent   = False
    # arch_dependent = True  
   
# class egg_qhull(BaseEggBuilder): 
    # license = "GNUPlot license"
    # authors = "Copyright (c) 1993-2011 C.B. Barber, Arlington, MA and The Geometry Center, University of Minnesota"
    # description = "Windows gcc libs and includes of qhull"
    # py_dependent   = False
    # arch_dependent = True  
   
class egg_rpy2(BaseEggBuilder): 
    license = "AGPLv3.0 (except rpy2.rinterface: LGPL)"
    authors = "Laurent Gautier"
    description = "Unofficial Windows gcc libs and includes of rpy2"
    py_dependent   = True
    arch_dependent = True
    
    def script_substitutions(self):
        from setuptools import find_packages
        rpy2_ = rpy2()
        return dict(URL          = "http://rpy.sourceforge.net",
                    PACKAGES     = find_packages(rpy2_.installdir,"rpy2"),
                    PACKAGE_DIRS = { "rpy2": pj(rpy2_.installdir, "rpy2") },
                    VERSION      = rpy2_.version+".rev"+rpy2_.revision,
                    PACKAGE_DATA = {'' : [Pattern.pyext]},
                    ) 

    
############################################################
# The following egg builders require that you have the     #
# corresponding library installed. This is because they    #
# are too difficult to compile and that we don't actually  #
# need to compile them (no linkage from us to them)        #
# or that they come as .exes and not eggs already          #
############################################################
class egg_numpy(InstalledPackageEggBuilder):
    license = "Numpy License"
    authors = "(c) Numpy Developers"
    description = "Numpy packaged as an egg"      
    py_dependent   = True
    arch_dependent = True    
    def script_substitutions_2(self):
        return dict( VERSION = self.package.version.full_version )
        
class egg_scipy(InstalledPackageEggBuilder):
    license = "Scipy License"
    authors = "(c) Enthought"
    description = "Scipy packaged as an egg"  
    py_dependent   = True
    arch_dependent = True        
    def script_substitutions_2(self):
        return dict( VERSION = self.package.version.full_version )
        
class egg_matplotlib(InstalledPackageEggBuilder):
    license = "Python Software Foundation License Derivative - BSD Compatible."
    authors = "Matplotlib developers"
    description = "Matplotlib packaged as an egg"  
    py_dependent   = True
    arch_dependent = True        
    def script_substitutions_2(self):        
        return dict( VERSION = self.package.__version__ )
                                               
class egg_PIL(InstalledPackageEggBuilder):
    license = "PIL License."
    authors = "Copyright (c) 1997-2011 by Secret Labs AB, Copyright (c) 1995-2011 by Fredrik Lundh."
    description = "PIL packaged as an egg"  
    __modulename__  = "Image"
    py_dependent   = True
    arch_dependent = True    
    def script_substitutions_2(self):
        return dict( VERSION = self.module.VERSION )
                 
class egg_pylsm(InstalledPackageEggBuilder):
    license = "PYLSM License."
    authors = "Freesbi.ch"
    description = "Patched version of PyLSM"  
    py_dependent   = True
    arch_dependent = False
    
    @property 
    @with_original_sys_path
    def package(self):
        return __import__(self.packagename)
    
    def script_substitutions_2(self):
        pth = self.package.__path__[0]
        version = "0.1-r34"
        for p in pth.split("\\"):
            if ".egg" in p:
                version = p.split("-")[1]+"_1" # we have a patched version
        return dict( VERSION = version )        
        
# class egg_pylibtiff(InstalledPackageEggBuilder):
    # license = "BSD License."
    # authors = "Pearu Peterson & friends."
    # description = "Precompiled pylibtiff for Windows."  
    # py_dependent   = True
    # arch_dependent = False
