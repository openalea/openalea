


canonical_dependencies = {
    "openalea" : ["pyqt4", "numpy", "scipy", "matplotlib"],
    "vplants" : ["openalea", "pyqt4", "boostpython", "qhull", "cgal", "glut"],
    "vplants-dev" : ["vplants", "pyqt4-dev", "sip4-devel", "qhull-dev", 
                     "cgal-dev", "boostpython-devel", "glut-dev", 
                     "compilers", "bisonflex"],
    "alinea" : ["vplants-dev", "openalea"]
}
                  
distribution_canonical_mappings = {
    "bisonflex" : {"ubuntu fedora" : "bison flex"},
    "boostpython" : {"ubuntu" : "libboost-python"},
    "boostpython-devel" : {"ubuntu" : "libboost-python-dev"},    
    "cgal" : {"ubuntu" : "libcgal"},
    "cgal-dev" : {"ubuntu" : "libcgal-dev"},
    "compiler" : { "ubuntu" : "g++ gfortran" },
    "glut" : {"ubuntu" : "libglut"},
    "glut-dev" : {"ubuntu" : "libglut-dev"},
    "matplotlib" : {"ubuntu" : "python-matplotlib"},
    "numpy" : {"ubuntu" : "python-numpy"},
    "pyqt4" : { "ubuntu" : "python-qt4", "fedora": "PyQt4" },
    "pyqt4-dev" : { "ubuntu" : "python-qt4-dev", "fedora": "PyQt4-devel" },
    "qhull" : {"ubuntu" : "libqhull"},
    "qhull-dev" : {"ubuntu" : "libqhull-dev"},
    "scipy" : {"ubuntu" : "python-scipy"},
} 

distribution_canonical_blacklists = {
    "boostpython" : {"karmic":"egg-boostpython"},
    "cgal-dev" : {"karmic": None},
}

