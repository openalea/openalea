import sys, os
from os.path import exists, join as pj
import shutil, glob, string


goodOptions = set([ "pyMaj",
                    "pyMin",
                    "srcDir",
                    "eggGlobs"])
                
easyFilenamesMap = {"pythonInst":"python.msi",
                    "setuptoolsInst":"setuptools.exe",
                    "pywin32Inst":"pywin32.exe",
                    "pyqt4Inst":"pyqt4.exe"}

def print_usage():
    msg="""
makeWinInstaller pyMaj=2 pyMin=6 srcDir=%HOMEPATH%\Downloads\ eggGlobs="Openalea*.egg"

You can have multiple globs, just use: eggGlobs="Openalea*.egg|Vplants*.egg".
The glob will be mangled with to incorporate python version information so you
should NOT write "Openalea*py2.6.egg" because it will be done automatically.
"""
    print msg


def get_wd(options):
    pyMaj, pyMin = options["pyMaj"], options["pyMin"]
    instDir = pj(os.getcwd(), pyMaj+"."+pyMin)
    return instDir

def prepare_working_dir(options):
    instDir = get_wd(options)
    if exists(instDir):
        shutil.rmtree(instDir, ignore_errors=True)
    os.mkdir(instDir)    

def copy_installer_files(options):
    print "Copying binaries..."
    for fk, ef in easyFilenamesMap.iteritems():
        src, dst = options[fk], pj(get_wd(options), ef)
        print "\t"+src+" => "+dst+"...",
        shutil.copyfile(src, dst)
        print "ok"

    print "Copying environment testing scripts..."
    test_scripts = glob.glob("*_test.py")
    for f in test_scripts:
        src, dst = f, pj(get_wd(options), f)
        print "\t"+src+" => "+dst+"...",
        shutil.copyfile(src, dst)
        print "ok"

def copy_eggs(options):
    globs = options["eggGlobs"]
    files = []
    for g in globs:
        files += glob.glob(g)
    print "Copying egg..."
    for f in files:
        src, dst = f, pj(get_wd(options), f)
        print "\t"+src+" => "+dst+"...",
        shutil.copyfile(src, dst)
        print "ok"
    options["eggs"] = files
        
def configure_inno_setup(options):
    print "Configuring inno script...",
    f = open("oawininst.iss.in")
    s = f.read()
    f.close()

    template = string.Template(s)
    eggs = options["eggs"]
    eggnum = str(len(eggs)-1)

    eggArrayInit = ""
    visualeaId = 0
    for i, e in enumerate(eggs):
        eggArrayInit+="Eggs[%i] := '%s';\n"%(i, e)
        if "Visualea" in e:
            visualeaId = str(i)
            
    s = template.substitute(#configure Python Major and Minor
                            PYTHONMAJOR=options["pyMaj"],
                            PYTHONMINOR=options["pyMin"],
                            #configure number of eggs
                            EGGMAXID=eggnum,
                            #configure the initialisation of egg array
                            EGGINIT=eggArrayInit,
                            VISUALEAEGGID=visualeaId)
                            
    f = open( pj(get_wd(options), "oawininst.iss"), "w" )
    f.write(s)
    f.close()
    print "ok"


def make_stitcher(options):
    pyfix = "py"+options["pyMaj"]+"."+options["pyMin"]
    def __stitch_egg_names(eggName):
        part = eggName.partition(".egg")
        return part[0] + pyfix + part[1]
    return __stitch_egg_names

if __name__ == "__main__":    
    options = dict(map(lambda x: x.split('='), sys.argv[1:]))

    if not set(options.iterkeys()) == goodOptions:
        print_usage()
        sys.exit(-1)

    srcDir = options["srcDir"]
    pyMaj  = options["pyMaj"]
    pyMin  = options["pyMin"]
    options["pythonInst"]     = glob.glob(pj(srcDir,"python*"+pyMaj+"."+pyMin+"*.msi"))[0]
    options["setuptoolsInst"] = glob.glob(pj(srcDir,"setuptools*py*"+pyMaj+"."+pyMin+"*.exe"))[0]
    options["pywin32Inst"]    = glob.glob(pj(srcDir,"pywin32*py*"+pyMaj+"."+pyMin+"*.exe"))[0]
    options["pyqt4Inst"]      = glob.glob(pj(srcDir,"PyQt*"+pyMaj+"."+pyMin+"*.exe"))[0]

    options["eggGlobs"] = map(make_stitcher(options), options["eggGlobs"].split("|"))
    print options["eggGlobs"]

    prepare_working_dir(options)
    copy_installer_files(options)
    copy_eggs(options)
    configure_inno_setup(options)
    print "Done"
