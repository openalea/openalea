"""
Automatic Ubuntu release

define a list of packages with their revision
dch --distribution precise -v 1.0.1~ppa1

:Exemple:
    
    >>> import ubuntu_release as ur
    >>> ur.openalea(distribution='precise', my_path='openalea1.0', dry_run=False)
"""
import os
from collections import OrderedDict
from path import path


##########################################################################
# Commands 
##########################################################################

# version 1.0.0~ppa1
VERSION = '1.0.1~ppa7'
cmd_dch = "dch -b --distribution %s -v %s"
cmd_debuild = "debuild -S -k1CF03DFF"
# name openalea, vplants, alinea
cmd_dput = 'dput ppa:christophe-pradal/%s '

#############################
# create vplants packages
def openalea_pkgs():
    pkgs = """
deploy
misc
deploygui
core
grapheditor
stdlib
visualea
sconsx
pkg_builder
numpy
scheduler
image
pylab
openalea_meta
"""
    #secondnature
    #openalea_dev

    pkgs = filter(None, pkgs.split('\n'))
    pkgs = OrderedDict.fromkeys(pkgs,VERSION)
    return pkgs

def openalea_name():
    """ Return the unique patterns of vplants changes names. """
    pkgs = """
deploy
misc
deploygui
core
grapheditor
stdlib
visualea
sconsx
pkgbuilder
numpy
scheduler
image
pylab
openalea
"""
    pkgs = filter(None, pkgs.split('\n'))

    return pkgs

#############################
# create vplants packages
def vplants_pkgs():
    pkgs = """
tool
PlantGL
stat_tool
sequence_analysis
amlobj
mtg
tree_matching
aml
tree
tree_statistic
fractalysis
lpy
container
newmtg
WeberPenn
tree_matching2
phyllotaxis_analysis
vplants_meta
vplants_dev
aml2py
"""
    #TODO: flowerdemo

    pkgs = filter(None, pkgs.split('\n'))
    pkgs = OrderedDict.fromkeys(pkgs,VERSION)
    pkgs['PlantGL']="2.16.1~ppa3"
    pkgs['lpy']="2.1.0~ppa3"
    pkgs['container']="2.2.0~ppa2"
    return pkgs

#############################
# create tissue packages
def tissue_deps_pkgs():
    pkgs = """
pglviewer
svgdraw
mechanics
physics
"""
    pkgs = filter(None, pkgs.split('\n'))
    pkgs = OrderedDict.fromkeys(pkgs,VERSION)
    return pkgs

def tissue_pkgs():
    pkgs = """
celltissue
genepattern
growth
tissueedit
tissueshape
tissueview
vmanalysis
tissue_meta
"""
    pkgs = filter(None, pkgs.split('\n'))
    pkgs = OrderedDict.fromkeys(pkgs,VERSION)
    return pkgs

def alinea_pkgs():
    pkgs = """
caribu
adel
graphtal
leafOptical
nema
pyratp
topvine
alinea_meta
"""
    pkgs = filter(None, pkgs.split('\n'))
    pkgs = OrderedDict.fromkeys(pkgs,VERSION)
    pkgs['caribu']="6.0.3~ppa1"
    return pkgs

def vplants_name():
    """ Return the unique patterns of vplants changes names. """
    pkgs_name = """
-tool
plantgl
stattool
sequenceanalysis
amlobj
vplants-mtg
treematching
aml
tree
treestatistic
fractalysis
lpy
container
openalea-mtg
weberpenn
treematching2
phyllotaxis
aml2py
vplants
"""
    # TODO: vplants_dev, flowerdemo
    pkgs_name = filter(None, pkgs_name.split('\n'))
    return pkgs_name

def my_dch(packages, my_path='.', distribution = 'precise', dry_run=False):
    """ run dch command on packages.
    packages is a dict with name:version
    """
    cwd = os.getcwd()
    os.chdir(my_path)
    for p, version in packages.iteritems():
        os.chdir(p)
        cmd = cmd_dch%(distribution,version)
        print "%s: \n"%p + '\t'+cmd
        if not dry_run:
            os.system(cmd)
        os.chdir('..')
    os.chdir(cwd)

def my_debuild(packages, my_path='.', dry_run=False):
    """ run dch command on packages.
    packages is a dict with name:version
    """
    cwd = os.getcwd()
    os.chdir(my_path)
    for p in packages:
        os.chdir(p)
        print "%s: \n"%p + '\t'+cmd_debuild
        if not dry_run:
            os.system(cmd_debuild)
        os.chdir('..')
    os.chdir(cwd)

def my_dput(packages, dist = 'openalea', my_path='.', dry_run=False):
    """ Run dput for upload files on launchpad """
    cwd = os.getcwd()
    os.chdir(my_path)
    errors = []
    d = path('.')
    for p in packages:
        files = d.files('*%s_*.changes'%p)
        changes = sorted([str(f) for f in files])
        if not changes:
            print "ERROR: %s not found"%p
            errors.append(p)
            continue
        print '\n ', p
        print changes
        my_file = changes[-1]
        print my_file

        cmd = cmd_dput%(dist,) + my_file
        print cmd 
        if not dry_run:
            os.system(cmd)
        print '#####################'

    print '\n'.join(errors)
    os.chdir(cwd)
    return

def openalea(distribution='precise',my_path='.', dry_run=True):
    oa_pkgs = openalea_pkgs()
    my_dch(oa_pkgs, my_path=my_path, distribution=distribution, dry_run=dry_run)
    my_debuild(oa_pkgs, my_path=my_path, dry_run=dry_run)
    names = openalea_name()
    my_dput(names, dist='openalea', my_path=my_path, dry_run=dry_run)

def vplants(distribution='precise',my_path='.', dry_run=True):
    vp_pkgs = vplants_pkgs()
    my_dch(vp_pkgs, my_path=my_path, distribution=distribution, dry_run=dry_run)
    my_debuild(vp_pkgs, my_path=my_path, dry_run=dry_run)
    names = vplants_name()
    my_dput(names, dist='vplants', my_path=my_path, dry_run=dry_run)

def tissue(distribution='precise',my_path='.', dry_run=True):
    td_pkgs = tissue_deps_pkgs()
    my_dch(td_pkgs, my_path=my_path, distribution=distribution, dry_run=dry_run)

    pkgs = tissue_pkgs()
    tissue_path = path(my_path)/'tissue'
    my_dch(pkgs, my_path=tissue_path, distribution=distribution, dry_run=dry_run)


    my_debuild(td_pkgs, my_path=my_path, dry_run=dry_run)
    my_debuild(pkgs, my_path=tissue_path, dry_run=dry_run)

    names = list(td_pkgs)
    my_dput(names, dist='vplants', my_path=my_path, dry_run=dry_run)

    tissue_names = list(pkgs)
    tissue_names[names.index('tissue_meta')]='tissue'
    my_dput(tissue_names, dist='vplants', my_path=tissue_path, dry_run=dry_run)

def alinea(distribution='precise',my_path='.', dry_run=True):
    pkgs = alinea_pkgs()
    my_dch(pkgs, my_path=my_path, distribution=distribution, dry_run=dry_run)
    my_debuild(pkgs, my_path=my_path, dry_run=dry_run)
    names = list(pkgs)
    names[names.index('alinea_meta')]='alinea'
    names[names.index('leafOptical')]='leafoptical'
    my_dput(names, dist='alinea', my_path=my_path, dry_run=dry_run)

"""
import ubuntu_release as ur

distribution='precise'
my_path='.'
dry_run=True

vp_pkgs = ur.vplants_pkgs()
VERSION = '1.0.1~ppa2'
ur.my_debuild(vp_pkgs, my_path=my_path, dry_run=dry_run)
names = ur.vplants_name()
ur.my_dput(names, dist='vplants', my_path=my_path, dry_run=dry_run)
"""

"""
import ubuntu_release as ur
distribution='precise'
my_path='release1.0/openalea'
dry_run=True
pkgs = '''
misc
deploygui
visualea
numpy
'''
VERSION = '1.0.1~ppa2'
oa_pkgs = filter(None, pkgs.split('\n'))
oa_pkgs = OrderedDict.fromkeys(oa_pkgs,VERSION)
oa_pkgs['deploygui']='1.0.1~ppa5'
oa_pkgs['visualea']='1.0.1~ppa4'
ur.my_dch(oa_pkgs, my_path=my_path, distribution=distribution, dry_run=dry_run)

"""
