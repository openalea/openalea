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



def get_packages(project):
    return package_lists.get(project, [])
    # TODO : go to look for them in the repositories!
    # mod_dict = {}
    # with download_package_file(project) as mod_file:
        # obj_code = compile(mod_file.read(), project, "exec")
        # mod = eval(obj_code, {}, mod_dict)

def svn_branch_exists(branch, version):
    sub = dict(svnexec=svn_exec, branchbase=branch,version=version)
    cmd = "%(svnexec)s info %(branchbase)s/release_%(version)s@HEAD"%sub    
    ret = subprocess.call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # svn returns 0 if the branch exists.    
    return ret==0
    
def svn_remove_branch(branch, version, not_dry_run, silent):
    sub = dict(svnexec=svn_exec, branchbase=branch,version=version)
    cmd = "%(svnexec)s remove %(branchbase)s/release_%(version)s -m \"removing release_%(version) branch.\""%sub
    if not silent: print cmd
    if not_dry_run: 
        return subprocess.call(cmd) == 0
    else:
        return True
    
def svn_copy_node(trunk, branchbase, version, node, rev, not_dry_run, silent ):
    sub = dict(svnexec=svn_exec, trunk=trunk, node=node, revision=rev, branchbase=branchbase, version=version)
    # TODO: ERROR HANDLING!    
    # let's obtain info to feed into the log message
    infocmd = "%(svnexec)s info %(trunk)s/%(node)s@%(revision)s"%sub
    pop     = subprocess.Popen(infocmd, stdout=subprocess.PIPE)
    info, err    = pop.communicate()
        
    sub["info"] = info
    
    # let's branch!
    cmd = "%(svnexec)s copy %(trunk)s/%(node)s@%(revision)s %(branchbase)s/release_%(version)s/%(node)s -m \"%(info)s\""%sub
    if not silent: print cmd
    if not_dry_run:
        return subprocess.call(cmd)==0  
    else:
        return True

def svn_mkdir(dir, not_dry_run, silent):
    sub = dict(svnexec=svn_exec, dir=dir)
    cmd = "%(svnexec)s mkdir %(dir)s -m \"creating %(dir)s directory.\""%sub
    if not silent: print cmd
    if not_dry_run:
        return subprocess.call(cmd)==0  
    else:
        return True
    
def svn_branch_project(project, version, delete_existing, not_dry_run, silent):
    verbose = not silent
    packages = get_packages(project)
    
    trunk, branchbase = projects.get(project, (None, None))
   
    exists = svn_branch_exists(branchbase, version)
    if exists:
        if verbose: 
            print "Release branch for version %s of %s already exists"%(version, project)    
        if delete_existing:
            if verbose: 
                print "Removing branch for version %s of %s"%(version, project)
            svn_remove_branch(branchbase, version, not_dry_run, silent)
        else:
            return None
    
    if not_dry_run:
        assert not svn_branch_exists(branchbase, version)
    
    svn_mkdir( "/".join([branchbase, "release_"+version]), not_dry_run, silent)
        
    ret_dict = {}
    for pack, rev in packages:
        if verbose: 
            print "Processing", pack, "" if not_dry_run else "for fake"
        ret_dict[pack] = svn_copy_node(trunk, branchbase, version, pack, rev, not_dry_run, silent)

    # copy multisetup
    success = svn_copy_node(trunk, branchbase, version, "multisetup.py", rev, not_dry_run, silent)
    
    return ret_dict
        
        
    
def _parse_version(version):
    return version.replace(".", "_")
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Manage branches and tags for releases on the server side.",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,)
                                     
    parser.add_argument("--svndir", default=os.curdir, help="path to %s executable"%svn_exec,
                        type=abspath)
                        
    parser.add_argument("--delete-existing", action="store_const", const=True, default=False, help="If the branch already exists, delete it.")                                    
    
    parser.add_argument("--login", default=None, help="login to connect to GForge.")
    parser.add_argument("--passwd", default=None, help="password to connect to GForge.")
    
    parser.add_argument("--not-dry-run", action="store_const", const=True, default=False, help="Don't do anything but print.")
    parser.add_argument("--silent", action="store_const", const=True, default=False, help="Don't print anything.")
    
    parser.add_argument("project", default=None, help="Which project to branch.", choices=["openalea","vplants"])
    parser.add_argument("version", default=None, help="Version of the branch.", type=_parse_version)
    
    return parser.parse_args()
    
def main():
    args = parse_arguments()
    os.environ["PATH"] += os.pathsep.join( [os.environ["PATH"], args.svndir] )
    if not has_svn():
        print "svn command in not available"        
        
    if not svn_branch_project(args.project, args.version, args.delete_existing, args.not_dry_run, args.silent):
        print "svn operation failed"
    
if __name__ == "__main__":
    main()