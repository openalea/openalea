# -*- python -*-
#
#       Branches VirtualPlant projects for releases
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
###############################################################################

__revision__ = "$Id$"
url = " $URL$ "

import os
import argparse
import tarfile
import fnmatch
import platform
import subprocess
from os.path import join as pj, abspath
from collections import namedtuple
from openalea.deploy.gforge_util import gforge_login

svn_exec = "svn.exe" if platform.system() == "Windows" else "svn"

ProjectAdresses = namedtuple("ProjectAdresses", "trunk branch")

projects = {
            "openalea": ProjectAdresses("https://scm.gforge.inria.fr/svn/openalea/trunk",
                                        "https://scm.gforge.inria.fr/svn/openalea/branches"),
            "vplants": ProjectAdresses("https://scm.gforge.inria.fr/svn/vplants/vplants/trunk",
                                       "https://scm.gforge.inria.fr/svn/vplants/vplants/branches"),
            "alinea": ProjectAdresses("https://scm.gforge.inria.fr/svn/openaleapkg/trunk",
                                       "https://scm.gforge.inria.fr/svn/openaleapkg/branches")
           }


# -- LISTS TO UPDATE --
# Here we list for each project the packages to branch.
# for each package we specify the revision at which we want to 
# branch.
package_lists = { 
                 "openalea": [ 
                             ("core", "HEAD"),
                             ("demo", "HEAD"),
                             ("deploy", "HEAD"),
                             ("deploygui", "HEAD"),
                             ("doc", "HEAD"),
                             ("grapheditor", "HEAD"), 
                             ("image", "HEAD"),
                             ("misc", "HEAD"), 
                             ("numpy", "HEAD"),
                             ("pkg_builder", "HEAD"),
                             ("pylab", "HEAD"),
                             ("scheduler", "HEAD"),
                             ("sconx", "HEAD"),
                             ("starter", "HEAD"),
                             ("stdlib", "HEAD"),
                             ("visualea", "HEAD"),    
                             ("openalea_meta", "HEAD"),
                             ],
                             
                 "vplants": [
                            ("aml", "HEAD"),
                            ("aml2py", "HEAD"),
                            ("amlobj", "HEAD"),
                            ("container", "HEAD"),
                            ("cmechanics", "HEAD"),
                            ("cphysics", "HEAD"),
                            ("fractalysis", "HEAD"),
                            ("lpy", "HEAD"),
                            ("mechanics", "HEAD"),
                            ("mtg", "HEAD"),
                            ("newmtg", "HEAD"),
                            ("phyllotaxis_analysis", "HEAD"),
                            ("physics", "HEAD"),
                            ("PlantGL", "HEAD"),
                            ("pglviewer", "HEAD"),
                            ("sequence_analysis", "HEAD"),
                            ("stat_tool", "HEAD"),
                            ("svgdraw", "HEAD"),
                            ("tissue", "HEAD"),
                            ("tool", "HEAD"),
                            ("tree", "HEAD"),
                            ("tree_matching", "HEAD"),
                            ("tree_matching2", "HEAD"),
                            ("tree_statistic", "HEAD"),
                            ("WeberPenn", "HEAD"),
                            ("vplants_meta", "HEAD"),
                            ],
                             
                 "alinea": [
                            ("caribu", "HEAD"),
                            ("graphtal", "HEAD"),
                            ("adel", "HEAD"),
                            ("../topvine", "HEAD"),
                            ("alinea_meta", "HEAD"),
                            ("leafOptical", "HEAD"),
                            ]
                }
# -- END LISTS TO UPDATE --
                
                
                


#################
# SVN Functions #
#################  
def has_svn(paths = []):    
    paths = paths+os.environ["PATH"].split(os.pathsep)
    for p in paths:
        subfiles = [f.lower() for f in os.listdir(p)]
        if svn_exec in subfiles:
            return pj(p, svn_exec)
    return None

    
def download_packages_file(project):
    pass

def get_packages(project):
    return package_lists.get(project, [])
    # TODO : go to look for them in the repositories!
    # mod_dict = {}
    # with download_package_file(project) as mod_file:
        # obj_code = compile(mod_file.read(), project, "exec")
        # mod = eval(obj_code, {}, mod_dict)
        
def branch_path(project, version, package=None, rev=None):
    trunk, branchbase = projects.get(project, (None, None))
    sub = dict(branchbase=branchbase, version=version, pack=package, rev=rev)
    pth = "%(branchbase)s/release_%(version)s"
    if package: pth+="/%(pack)s"
    if rev: pth+="@%(rev)s"
    return pth%sub
    
def tag_path(project, version, package=None, rev=None):
    trunk, tagbase = projects.get(project, (None, None))
    if tagbase:
        tagbase = tagbase.replace("branches", "tags")
    sub = dict(tagbase=tagbase, version=version, pack=package, rev=rev)
    pth = "%(tagbase)s/release_%(version)s"
    if package: pth+="/%(pack)s"
    if rev: pth+="@%(rev)s"
    return pth%sub
    
def trunk_path(project, package=None, rev=None):
    trunk, branchbase = projects.get(project, (None, None))    
    if package.startswith(".."):
        # go up in trunk base:
        trunk = trunk[:trunk.rindex("/")] # remove the trailing directory from trunk path
        package = package[3:] # remove "../" from package
    sub = dict(trunk=trunk, pack=package, rev=rev)
    pth = "%(trunk)s"
    if package: pth+="/%(pack)s"
    if rev: pth+="@%(rev)s"
    return pth%sub

def svn_path_exists(path, revision="HEAD", peg="HEAD"):
    sub = dict(svnexec=svn_exec, path=path)
    cmd = "%(svnexec)s info %(path)s@HEAD"%sub
    ret = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    return ret==0 # svn returns 0 if the path exists.    
    
def svn_remove_path(path):
    sub = dict(svnexec=svn_exec, path=path)
    cmd = "%(svnexec)s remove %(path)s -m \"removing %(path)s branch.\""%sub
    print cmd
    return dr_call(cmd) == 0
    
def svn_copy_path(src, tgt, revision="HEAD", peg="HEAD"):
    sub = dict(svnexec=svn_exec, src=src, tgt=tgt)
    # TODO: ERROR HANDLING!    
    # let's obtain info to feed into the log message
    infocmd = "%(svnexec)s info %(src)s"%sub
    # don't use dry_popen as we want to see the output
    pop     = subprocess.Popen(infocmd, stdout=subprocess.PIPE)
    info, err    = pop.communicate()
        
    sub["info"] = info
    
    # let's branch!
    cmd = "%(svnexec)s copy %(src)s %(tgt)s -m \"%(info)s\""%sub
    print cmd, "\n"
    return dr_call(cmd)==0

def svn_mkdir(direct):
    sub = dict(svnexec=svn_exec, dir=direct)
    cmd = "%(svnexec)s mkdir --parents %(dir)s -m \"creating %(dir)s directory.\""%sub
    print cmd
    return dr_call(cmd)==0  
    
def __svn_del_path_if_exists(path, delete_existing):
    exists = svn_path_exists(path)
    if exists:
        print "Path %s already exists"%path    
        if delete_existing:
            print "Removing %s"%path
            svn_remove_path(path)
        else:
            return None
import sys        
def svn_branch_project(project, version, delete_existing, 
                       packages=None, branch_can_exist=False, no_multisetup=False, tag=False):   
    if not packages:
        packages = get_packages(project)
    
    if tag:
        branchpath = tag_path(project, version)
    else:
        branchpath = branch_path(project, version)
    
    if not branch_can_exist:
        __svn_del_path_if_exists( branchpath, delete_existing)
        #sys.exit(-1)
        if not_dry_run:
            assert not svn_path_exists(branchpath)
        svn_mkdir( branchpath )
        
    ret_dict = {}
    for pack, rev in packages:
        print "Processing", pack, "" if not_dry_run else "for fake"
        if tag:
            src = branch_path( project, version, pack, rev )
        else:
            src = trunk_path( project, pack, rev )
        ret_dict[pack] = svn_copy_path(src, branchpath)

    # copy multisetup
    if not no_multisetup:
        pth = trunk_path( project, "multisetup.py" )
        success = svn_copy_path(pth, branchpath)
    
    return ret_dict
        
def svn_update_package(project, version, packages, working_copy, auto_commit=False):
    for pack, rev in packages:
        trunkpath  = trunk_path(project, pack)
        if ":" in rev: #merge a range
            cmd = "%(svnexec)s merge -r %(rev)s %(trunk)s %(branch)s"
        elif "," in rev: #cherry picking
            cmd = "%(svnexec)s merge -c %(rev)s %(trunk)s %(branch)s"
        else:  #use mergeinfo
            cmd = "%(svnexec)s merge %(trunk)s %(branch)s"
        
        subd = dict(svnexec=svn_exec,  rev=rev, trunk=trunkpath, branch=working_copy+"/"+pack)
        cmd = cmd%subd
        print cmd
        pop = dr_popen(cmd, stdout=subprocess.PIPE)
        txt, err = pop.communicate()        
        ret = pop.returncode
        print txt
        if ret != 0:
            return False
        if auto_commit:
            ret = svn_commit(working_copy, txt)
        else:
            fname = pj(working_copy, "merge_log_%s.txt"%pack)
            with open( fname, "w" ) as f:
                f.write(txt)
                print "Possible commit log written to:", fname
        if ret:
            return False
    return True
    
def svn_commit(working_copy, message):
    subd = dict(svnexec=svn_exec,  wc=working_copy, message=message)
    cmd = "%(svnexec)s ci %(wc)s -m \"%(message)s\""%subd
    return dr_call(cmd) == 0


def svn_export_project(project, version, working_copy):
    project_ver = project+"_"+version
    project_exp = project+"_"+version+"_exp"
    subd = dict(svnexec=svn_exec,  wc=working_copy, proj=project_exp)
    cmd = "%(svnexec)s export %(wc)s %(proj)s"%subd
    if dr_call(cmd) == 0:
        tarf = project_ver+".tar.gz"
        print "create tarfile", tarf
        if not_dry_run:
            try:
                with tarfile.open(tarf, "w:gz") as tar:
                    tar.add( pj(working_copy, project_exp), arcname=project )
            except Exception, e:
                print e
                return -1
            else:
                return 0
        else:
            return 0
    else:
        return -1
        
#######################
# MAIN AND PARSE ARGS #
#######################
# -- Argument parsing will set this to True or False --
not_dry_run = True
# -- The following will be substituted by 
# no op functions if not_dry_run is True --
dr_call  = subprocess.call
dr_popen = subprocess.Popen

# -- No op functions used when not_dry_run is False --
def dry_call(*args, **kwargs):
    print "dry_call", args, kwargs
    return 0
    
class dry_popen(object):
    def __init__(self, *args, **kwargs):
        print "dry_popen", args, kwargs
        self.returncode = 0
    
    def communicate(self, *args, **kwargs):
        print "dry_popen.communicate", args, kwargs
        return "", None
        
class NullOutput(object):
    def write(self, s):
        pass

def _parse_version(version):
    return version.replace(".", "_")
    
def _parse_package(pkg):
    pkg_rev = pkg.split("@")
    if len(pkg_rev) == 1:
        return pkg_rev[0], "HEAD"
    elif len(pkg_rev) == 2:
        return pkg_rev
    else:
        raise Exception("What is this : %s ??????"%pkg)        
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Manage branches and tags for releases on the server side.",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,)
                                     
    parser.add_argument("--svndir", default=os.curdir, help="path to %s executable"%svn_exec,
                        type=abspath)
                        
    parser.add_argument("--delete-existing", "-e", action="store_const", const=True, default=False, help="If the branch already exists, delete it.")                                    
    
    parser.add_argument("--login", default=None, help="login to connect to GForge.")
    parser.add_argument("--passwd", default=None, help="password to connect to GForge.")
    
    parser.add_argument("--not-dry-run", action="store_const", const=True, default=False, help="Actually do things! By default we just print comamnds.")
    parser.add_argument("--silent", "-s", action="store_const", const=True, default=False, help="Don't print anything.")
    
    parser.add_argument("project", default=None, help="Which project to branch.", choices=["openalea","vplants","alinea"])
    parser.add_argument("version", default=None, help="Version of the branch (ex: 1.0).", type=_parse_version)
    
    parser.add_argument("--package", "-p", action="append", help="Copy one specific package from project. package|package@revision", type=_parse_package, dest="packages")
    parser.add_argument("--ignore-rbase", "-r", action="store_const", const=True, default=False, 
                        help="Don't check if the destination root exists.")
    parser.add_argument("--no-multisetup", "-m", action="store_const", const=True, default=False, 
                        help="Don't copy multisetup.")    
    
    parser.add_argument("--tag", "-t", action="store_const", const=True, default=False, 
                        help="Create a tag for release.")

    parser.add_argument("--update-package", "-u", action="append", 
                        help="Syncs a branch package with the trunk. ROOT|ALL|package|package@revN:revM|package@revU,revW,revW", type=_parse_package, dest="update")
    parser.add_argument("--working-copy", "-w", default = None, help="Working copy to merge into", type=abspath)
    parser.add_argument("--auto-commit", "-a", action="store_const", const=True, default = False, help="Auto commit merges")
    parser.add_argument("--export-srcs", "-x", action="store_const", const=True, default = False, help="Create source tarball")
    return parser.parse_args()



   

def main():
    import sys
    import getpass
    global not_dry_run
    global dr_call
    global dr_popen
    
    args = parse_arguments()
    os.environ["PATH"] += os.pathsep.join( [os.environ["PATH"], args.svndir] )
    
    # OK, so this is used nowhere but somehow, it works... how did this happen?
    # Subversion probably cached my own login and password, and uses that to log in...
    if args.project != "openalea" : #then svn operations need password
        if args.login != None:
            if args.passwd is None:
                args.passwd = getpass.getpass("GForge password please: ")

    if not args.not_dry_run:
        print "Doing a dry run. Check that the command lines are correct then rerun with the --not-dry-run flag\n"
        not_dry_run = False
        dr_call  = dry_call
        dr_popen = dry_popen
    
        
    if not has_svn([args.svndir]):
        print "svn command in not available"

    if not args.working_copy and (args.update or args.export_srcs):
        print "Cannot merge export, no working copy given"
        sys.exit(-1)
        
    if args.silent:
        sys.stdout = NullOutput()        
    
    if args.export_srcs:
        sys.exit( 0 if svn_export_project(args.project, args.version, args.working_copy) else -1)        
        
    if args.update:
        if "ALL" in zip(*args.update)[0]:
            args.update = package_lists.get(args.project)
        elif "ROOT" in zip(*args.update)[0]:
            args.update = [("","")]
        sys.exit( 0 if svn_update_package(args.project, args.version, args.update, args.working_copy, args.auto_commit) else -1)
        
    if args.tag:
        if not svn_branch_project(args.project, args.version, args.delete_existing, 
                                  packages=args.packages,
                                  branch_can_exist=args.ignore_rbase,
                                  no_multisetup=args.no_multisetup, tag=True):
            print "svn tag operation failed"
    else:
        if not svn_branch_project(args.project, args.version, args.delete_existing, 
                                  packages=args.packages,
                                  branch_can_exist=args.ignore_rbase,
                                  no_multisetup=args.no_multisetup):
            print "svn branch operation failed"
        
if __name__ == "__main__":
    main()