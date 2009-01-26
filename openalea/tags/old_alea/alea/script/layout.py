"""
Script creating a valid OpenALEA package layout

Usage:
  python layout.py PKG_NAME [ src_subdirs ]

"""
from path import path
from sys import argv, exit
import re

good_name = re.compile( "[a-z]{5,}" )

here = path.getcwd()

# Argument parsing
if len( argv ) < 2:
  print """
Usage:
  python %s PKG_NAME [ src_subdirs ]
""" % (argv[0],)
  exit( 3 )

name = argv[ 1 ]

src_subdirs = argv[ 2: ]

#End Argument parsing

if not good_name.match( name ):
  print "Error, package name %s is invalid" % ( name, )
  exit( 1 )

pkg_dir = here / name

if pkg_dir.exists():
  print "Warning, the directory %s already exists" % ( pkg_dir, )
  answer = raw_input("Do you want still to continue ? (y/n)\n")
  if answer != "y":
    exit( 2 )
else:
  print "Creating %s ..." % ( pkg_dir, )
  pkg_dir.mkdir()

dirs = [
  pkg_dir/"src",
  pkg_dir/"wralea",
  pkg_dir/"doc",
  pkg_dir/"test",
  pkg_dir/"example"
  ]

for d in src_subdirs:
  dirs.append( ( pkg_dir/"src"/d ).normpath() )

for d in dirs:
  print "Creating %s ..." % ( d, )
  try:
    d.mkdir()
  except OSError, e:
    if e.args[ 0 ] != 17:
      raise

'''
init_py = pkg_dir/"__init__.py"
print "Creating %s ..." % ( init_py, )

f = file( init_py, "w" )
f.write( """
from os.path import join
__path__.append( join( __path__[ 0 ], "src" ) )
""")
f.close()
'''

files = [
  pkg_dir/"LICENSE.txt",
  pkg_dir/"README.txt",
  pkg_dir/"ChangeLog.txt",
  pkg_dir/"AUTHORS.txt",
  pkg_dir/"NEWS.txt",
  pkg_dir/"TODO.txt"
  ]

for f in files:
  print "Creating %s ..." % ( f, )
  f.touch()

