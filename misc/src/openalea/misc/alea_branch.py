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
                                       "https://scm.gforge.inria.fr/svn/vplants/vplants/branches")
           }

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
                            ]
                }

def has_svn(paths = []):    
    paths = os.environ["PATH"].split(os.pathsep)
    for p in paths:
        subfiles = [f.lower() for f in os.listdir(p)]
        if svn_exec in subfiles:
            return pj(p, svn_exec)
    return None

    
def download_packages_file(project):
    pass


def branch_path(project, version, package=None, rev=None):
    trunk, branchbase = projects.get(project, (None, None))
    sub = dict(branchbase=branchbase, version=version, pack=package, rev=rev)
    pth = "%(branchbase)s/release_%(version)s"
    if package: pth+="/%(pack)s"
    if rev: pth+="@%(rev)s"
    return pth%sub
    
def trunk_path(project, package=None, rev=None):
    trunk, branchbase = projects.get(project, (None, None))
    sub = dict(trunk=trunk, pack=package, rev=rev)
    pth = "%(trunk)s"
    if package: pth+="/%(pack)s"
    if rev: pth+="@%(rev)s"
    return pth%sub

def get_packages(project):
    return package_lists.get(project, [])
    # TODO : go to look for them in the repositories!
    # mod_dict = {}
    # with download_package_file(project) as mod_file:
        # obj_code = compile(mod_file.read(), project, "exec")
        # mod = eval(obj_code, {}, mod_dict)

def svn_path_exists(path):
    sub = dict(svnexec=svn_exec, path=path)
    cmd = "%(svnexec)s info %(path)s@HEAD"%sub
    ret = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
    return ret==0 # svn returns 0 if the path exists.    
    
def svn_remove_path(path, not_dry_run):
    sub = dict(svnexec=svn_exec, path=path)
    cmd = "%(svnexec)s remove %(path)s -m \"removing %(path) branch.\""%sub
    print cmd
    if not_dry_run: 
        return subprocess.call(cmd) == 0
    else:
        return True
    
def svn_copy_path(src, tgt, not_dry_run):
    sub = dict(svnexec=svn_exec, src=src, tgt=tgt)
    # TODO: ERROR HANDLING!    
    # let's obtain info to feed into the log message
    infocmd = "%(svnexec)s info %(src)s"%sub
    pop     = subprocess.Popen(infocmd, stdout=subprocess.PIPE)
    info, err    = pop.communicate()
        
    sub["info"] = info
    
    # let's branch!
    cmd = "%(svnexec)s copy %(src)s %(tgt)s -m \"%(info)s\""%sub
    print cmd
    if not_dry_run:
        return subprocess.call(cmd)==0  
    else:
        return True

def svn_mkdir(direct, not_dry_run):
    sub = dict(svnexec=svn_exec, dir=direct)
    cmd = "%(svnexec)s mkdir %(dir)s -m \"creating %(dir)s directory.\""%sub
    print cmd
    if not_dry_run:
        return subprocess.call(cmd)==0  
    else:
        return True

def __svn_del_path_if_exists(path, delete_existing, not_dry_run):
    exists = svn_path_exists(path)
    if exists:
        print "Path %s already exists"%path    
        if delete_existing:
            print "Removing %s"%path
            svn_remove_path(path, not_dry_run)
        else:
            return None
        
def svn_branch_project(project, version, delete_existing, not_dry_run, 
                       packages=None, branch_can_exist=False, no_multisetup=False):   
    if not packages:
        packages = get_packages(project)
    
    branchpath = branch_path(project, version)
    
    if not branch_can_exist:
        __svn_del_path_if_exists( branchpath, delete_existing, not_dry_run)
        if not_dry_run:
            assert not svn_path_exists(branchpath)
        svn_mkdir( branchpath, not_dry_run)
        
    ret_dict = {}
    for pack, rev in packages:
        print "Processing", pack, "" if not_dry_run else "for fake"
        src = trunk_path( project, pack, rev )
        ret_dict[pack] = svn_copy_path(src, branchpath, not_dry_run)

    # copy multisetup
    if not no_multisetup:
        pth = trunk_path( project, "multisetup.py" )
        success = svn_copy_path(pth, branchpath, not_dry_run)
    
    return ret_dict
        
        
#######################
# MAIN AND PARSE ARGS #
#######################

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
    
    parser.add_argument("project", default=None, help="Which project to branch.", choices=["openalea","vplants"])
    parser.add_argument("version", default=None, help="Version of the branch (ex: 1.0).", type=_parse_version)
    
    parser.add_argument("--package", "-p", action="append", help="Copy one specific package from project.", type=_parse_package, dest="packages")
    parser.add_argument("--ignore-rbase", "-r", action="store_const", const=True, default=False, 
                        help="Don't check if the destination root exists.")
    parser.add_argument("--no-multisetup", "-m", action="store_const", const=True, default=False, 
                        help="Don't copy multisetup.")
    
    return parser.parse_args()
    
def main():
    import sys

    args = parse_arguments()
    os.environ["PATH"] += os.pathsep.join( [os.environ["PATH"], args.svndir] )
    
    if not args.not_dry_run:
        print "Doing a dry run. Check that the command lines are correct then rerun with the --not-dry-run flag\n"

    if args.silent:
        sys.stdout = NullOutput()
        
    if not has_svn():
        print "svn command in not available"        
        
    if not svn_branch_project(args.project, args.version, args.delete_existing, 
                              args.not_dry_run,
                              packages=args.packages,
                              branch_can_exist=args.ignore_rbase,
                              no_multisetup=args.no_multisetup):
        print "svn operation failed"
    
if __name__ == "__main__":
    main()