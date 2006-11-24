import os

print "python setup.py --help-commands"
os.system("python setup.py --help-commands")
raw_input()

print "python setup.py build"
os.system("python setup.py build")
raw_input()

print "python setup.py build_namespace"
os.system("rm -Rf build")
os.system("python setup.py build_namespace")
raw_input()

print "python setup.py build_scons"
os.system("rm -Rf build")
os.system("python setup.py build_scons")
raw_input()

print "python setup.py build_scons --scons-ext-param='test=t test2=t2'"
os.system("rm -Rf build")
os.system("python setup.py build_scons --scons-ext-param='test=t test2=t2'")
raw_input()

print "python setup.py install"
os.system("rm -Rf build")
os.system("python setup.py install")
raw_input()

print "python setup.py install"
os.system("rm -Rf build")
os.system("python setup.py install --external-prefix=/usr/local/aotest")
raw_input()

print "python setup.py install_external_data"
os.system("rm -Rf build")
os.system("python setup.py install_external_data")
raw_input()

print "python setup.py install_external_data"
os.system("rm -Rf build")
os.system("python setup.py install_external_data --external-prefix=/usr/local/aotest")
raw_input()

print "python setup.py bdist"
os.system("rm -Rf build")
os.system("python setup.py bdist")
raw_input()


print "python setup.py bdist_rpm"
os.system("rm -Rf build")
os.system("python setup.py bdist_rpm")
raw_input()

print "python setup.py sdist"
os.system("rm -Rf build")
os.system("python setup.py sdist")
raw_input()

#os.system("rm -Rf build; rm -Rf dist")
