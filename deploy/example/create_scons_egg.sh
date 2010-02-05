!#/usr/bin/sh

SCONS=scons-1.2.0.d20100117
wget http://sourceforge.net/projects/scons/files/scons/1.2.0.d20100117/${SCONS}.tar.gz/download
tar xvfz ${SCONS}.tar.gz
cp setup_scons.py ${SCONS}/setup.py
cd ${SCONS}
python setup.py build;
python setup.py bdist_egg
