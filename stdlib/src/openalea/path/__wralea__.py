
# This file has been generated at Wed Apr 21 17:24:35 2010

from openalea.core import *


__name__ = 'openalea.path'

__editable__ = True
__description__ = 'File manipulation library.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__version__ = '0.0.1'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__icon__ = ''


__all__ = []

abspath = Factory(name='abspath',
                category='File,IO',
                nodemodule='paths',
                nodeclass='py_abspath',
                inputs=({'interface': IFileStr, 'name': 'path', 'value': '.'},),
                outputs=({'interface': IFileStr, 'name': 'path'},),
               )
__all__.append('abspath')

basename= Factory(name='basename',
                category='File,IO',
                nodemodule='paths',
                nodeclass='py_basename',
                inputs=({'interface': IFileStr, 'name': 'path', 'value': '.'},),
                outputs=({'interface': IFileStr, 'name': 'path'},),
               )
__all__.append('basename')

bytes= Factory(name='bytes',
                category='File,IO',
                nodemodule='paths',
                nodeclass='py_bytes',
                inputs=({'interface': IFileStr, 'name': 'path', 'value': '.'},),
                outputs=({'interface': IStr, 'name': 'content'},),
               )
__all__.append('bytes')

chmod = Factory(name='chmod',
                category='File,IO',
                nodemodule='paths',
                nodeclass='py_chmod',
                inputs=({'interface': IFileStr, 'name': 'path', 'value': '.'},
                dict(name='mode', interface=IInt,value=755)),
                outputs=({'interface': IFileStr, 'name': 'path'},),
               )
__all__.append('chmod')

chown = Factory(name='chown',
                category='File,IO',
                nodemodule='paths',
                nodeclass='py_chown',
                inputs=({'interface': IFileStr, 'name': 'path', 'value': '.'},
                dict(name='uid', interface=IInt), dict(name='gid', interface=IInt)),
                outputs=({'interface': IFileStr, 'name': 'path'},),
               )
__all__.append('chown')

copy = Factory(name='copy',
                category='File,IO',
                nodemodule='paths',
                nodeclass='py_copy',
                inputs=({'interface': IFileStr, 'name': 'src', 'value': '.'},
                {'interface': IFileStr, 'name': 'dest', 'value': '.'},),
                outputs=({'interface': IFileStr, 'name': 'path'},),
               )
__all__.append('copy')

copy_dir = Factory(name='copy (dir)',
                category='File,IO',
                nodemodule='paths',
                nodeclass='py_copy',
                inputs=({'interface': IFileStr, 'name': 'src', 'value': '.'},
                {'interface': IDirStr, 'name': 'dest', 'value': '.'},),
                outputs=({'interface': IFileStr, 'name': 'path'},),
               )
__all__.append('copy_dir')



"""
copy
copy2
copyfile
copymode
copystat
copytree
count
ctime
decode
dirname
dirs
drive
encode
endswith
exists
expand
expandtabs
expanduser
expandvars
ext
files
find
fnmatch
format
get_owner
getatime
getctime
getcwd
getmtime
getsize
glob
index
isabs
isalnum
isalpha
isdigit
isdir
isfile
islink
islower
ismount
isspace
istitle
isupper
join
joinpath
lines
link
listdir
ljust
lower
lstat
lstrip
makedirs
mkdir
move
mtime
name
namebase
normcase
normpath
open
owner
parent
partition
pathconf
read_md5
readlink
readlinkabs
realpath
relpath
relpathto
remove
removedirs
rename
renames
replace
rfind
rindex
rjust
rmdir
rmtree
rpartition
rsplit
rstrip
samefile
size
split
splitall
splitdrive
splitext
splitlines
splitpath
startswith
stat
statvfs
strip
stripext
swapcase
symlink
text
title
touch
translate
unlink
upper
utime
walk
walkdirs
walkfiles
write_bytes
write_lines
write_text
zfill
"""



