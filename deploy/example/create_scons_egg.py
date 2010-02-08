import os
import urllib
import tarfile
import shutil
from subprocess import call

SCONS='scons-1.2.0.d20100117'
target = 'http://sourceforge.net/projects/scons/files/scons/1.2.0.d20100117/%s.tar.gz/download'%(SCONS,)
archive = '%s.tar.gz'%SCONS

# wget scons from sourceforge
urllib.urlretrieve(target, archive)

# Extract the targz in the current directory
tar = tarfile.open(archive)
tar.extractall()
tar.close()

#cp setup_scons.py ${SCONS}/setup.py
shutil.copyfile('setup_scons.py', '%s/setup.py'%SCONS)
os.chdir(SCONS)

call(['python',  'setup.py', 'build'])
call(['python', 'setup.py', 'bdist_egg'])

print 'FINISHED'
