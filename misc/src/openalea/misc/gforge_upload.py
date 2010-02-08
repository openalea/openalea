"""A script to Query package information, create new packages/releases, a

upload all files within the OpenAlea website: http://openalea.gforge.inria.fr


.. todo::
    * if package is not provided, guess it from the name ?
    * add openalea:to*:0.1 -> bug warning: no create a to* package !!!
    * same for release....
    * use a function to uncomplicated the code

"""

__revision__ = " $Id$"

from optparse import OptionParser
from fnmatch import fnmatch
import glob
import os
from openalea.deploy.gforge import GForgeProxy, proc_id, type_id
try:
    from openalea.deploy.console import nocolor, color_terminal, green, red, bold, purple
except:
    red = green = bold = green = lambda x:x

import sys

#available_mode = ['query', 'add', 'remove', 'delete']
#available_project = ['openalea', 'vplants', 'alinea']

server = GForgeProxy()


class UploaderError(Exception):
    def __init__(self, msg):
        self.msg = msg


class Uploader(object):
    """A script to Query package information, create new packages/releases, and
        upload all files within the OpenAlea website: http://openalea.gforge.inria.fr

    :Example:

    >>> python gforge_upload --mode query --project openalea --package aml2py
    >>> python gforge_upload --mode add --glob  /home/user/*.egg --project openalea --package VPlants -release 0.8
    >>> python gforge_upload --mode remove --project openalea --packge VPlants --release 0.8 --glob *.egg

    type --help to get more help and usage

    """

    available_mode = ['query', 'add', 'remove', 'delete']
    available_project = ['openalea', 'vplants', 'alinea']

    def __init__(self, opts):
        """Initialization of project/package/release and file names
        path of directory where the files exist
        simulation mode
        """
        self.project = opts.project
        self.package = opts.package
        self.release = opts.release
        self.filename = opts.glob
        self.glob = opts.glob
        self.mode = opts.mode
        self.server = server
        self.server_packages = None
        self.server_releases = None
        self.server_files = None
        self.simulate = opts.dry_run
        self.dry_run = opts.dry_run
        self.login = opts.login
        self.password = opts.password
        if opts.non_interactive is True:
            self.interactive = False
        else:
            self.interactive = True



        self.check_project()
        #self.server.login(self.login, self.password)
        self.mylogin()

    def info(self):
        print 'GFORGE Uploading -----------------------------------'
        print 'Project: %s' % self.project
        print 'Package: %s' % self.package
        print 'Release: %s' % self.release
        print 'Filname(s): %s' %  self.glob

    def mylogin(self):
        """  Open a session """
        import getpass
        self.info()
        if(self.login is None):
            self.login = raw_input(green("Enter your GForge login:"))
        if(self.password is None):
            self.password = getpass.getpass(green("Enter you GForge password:"))

        self.server.login(self.login, self.password)
        if server.session is None:
            raise ValueError(red('Connection failed. check username and passord'))
            sys.exit(0)


    def __del__(self):
        """ Logout the session when this instance is deleted.

        """
        self.server.logout()

    def messages(self, elt, elements, element_name):
        """ Display the list of elements (e.g. package, release) which
        are on the server.

        :param elt: list of packages/releases or files on the server
        :param elements: packages/release or files
        :param element_name: string 'Packages'/'Release' or 'Files'

        """
        elt.sort()
        msg = '%s in the ' % element_name + elements + ' are :'
        underscore = '-' * len(msg)
        tab = '  '
        print msg
        print underscore
        print tab + ('\n' + tab).join(elt)


    def ask(self, question):
        """Return the response that is the result
        of evaluating the message.

        :param question: string

        """
        if self.interactive:
            ok = raw_input(question + " [y/n]  ")
            return ok.lower() == 'y'
        else:
            return True


    def file_type(self, filename):
        """ Retrieve the file type

        :param filename: file's name
        Return the file type ('.zip'/'.gz'/'.other'...)

        """
        f = os.path.splitext(filename)
        ft = f[1]
        if ft not in type_id.keys():
            ft = 'other'
        return ft


    def proc_type(self, filename):
        """ Retrieve the processor type

        :param filename: file's name
        Return the processor type ('i386'/'any'/'other')

        """
        win, linux, python = '*win32*', '*linux*', '*py*'

        if fnmatch(filename, win) or fnmatch(filename, linux):
            pt = 'i386'
        elif fnmatch(filename, python):
            pt = 'any'
        else:
            pt = 'other'
        return pt

    def check_project(self):
        if self.project not in self.available_project:
            print 'Error command : project must be either %s' % self.available_project
            sys.exit(0)


    def add_package(self):
        msg =  purple('Package %s not found in the %s project. ' % (self.package, self.project))
        msg += purple('Shall we add %s package in %s project ? ' % (self.package, self.project))
        if self.ask(msg):
            if self.dry_run:
                print 'Action skipped'
                pass
            else:
                self.server.add_package(self.project, self.package)
                print '%s package has been created on the server' % self.package
        else:
            print 'quitting'
            self.server.logout()
            sys.exit()


    def check_packages(self):
        self.check_project()
        packages = server.get_packages(self.project)
        packages.sort()
        self.server_packages = packages
        if self.package is None or self.package.startswith('-'):
            print red('you must provide a valid package with --package. Available packages are %s' % self.server_packages)
            sys.exit(0)
        if self.package not in self.server_packages:
            if self.mode == 'add':
                self.add_package()
            else:
                print red('Check your package name. Available packages are')
                for package in packages:
                    print '\t %s'  % package
                sys.exit(0)

    def add_release(self):
        msg = purple('Relase %s not found in package %s (%s project). ' % (self.release, self.package, self.project))
        msg += purple('Shall we add it the release %s release in %s package' % (self.release, self.package))
        if self.ask(msg):
            if self.dry_run:
                print 'Action skipped'
                pass
            else:
                self.server.add_release(self.project, self.package, self.release, 'notes', 'changes')
                print '%s release has been created on the server' % self.release
        else:
            print 'quitting'
            self.server.logout()

    def remove_file(self, file):
        """returns True if file removed"""
        msg = purple('GforgeUpload -- Removing file: %s will be removed (in %s). Shall we proceed ? ' % (os.path.basename(file), self.get_location()))
        if self.ask(msg):
            if self.dry_run:
                return True

            else:
                self.server.remove_file(self.project, self.package, self.release, os.path.basename(file))
            print '%s removed' % os.path.basename(file)
            return True
        else:
            print '%s not deleted as requested' % file
            return False


    def add_file(self, file):
        msg = purple('%s will be added to the gforge (in %s). Shall we proceed ? ' % (os.path.basename(file), self.get_location()))
        f_type = self.file_type(os.path.basename(file))
        p_type = self.proc_type(os.path.basename(file))
        if self.ask(msg):
            if self.dry_run:
                pass
            else:
                if os.path.getsize(file) > 2000000L:
                    self.server.add_big_file(self.project, self.package, self.release, 
                        file, p_type, f_type)
                else:
                    self.server.add_file(self.project, self.package, self.release, 
                        file, p_type, f_type)
            print '%s file has been uploaded on the server (in %s)' % (os.path.basename(file), self.get_location())
        else:
            print '%s not uploaded as requested' % file


    def check_releases(self):
        releases = server.get_releases(self.project, self.package)
        releases.sort()
        self.server_releases = releases
        if self.release is None:
            print 'you must provide release with --release. Available releases are %s' % self.server_releases
            sys.exit(0)
        if self.release not in self.server_releases:
            if self.mode == 'add':
                self.add_release()
            else:
                print red('Check your release name. Available releases are')
                for release in releases:
                    print '\t %s'  % release
                sys.exit(0)

    def check_files(self):
        files = server.get_files(self.project, self.package, self.release)
        self.server_files = files 
        if self.filename is None:
            print 'you must provide a glob filename with --glob. quitting'
            sys.exit(0)


    def query(self):
        """ Query the project, package, release.

        Use the check method to get the different elements exist on the server.
        Display a list of the element name which exists


        >>> python gforge_upload query openalea:aml2py
            Display the list of releases which exists in /aml2py package
                                                        /openalea project
                                                        /on the gforge server
        """

        self.check_project()
        if self.package  and self.release:
            self.check_packages()
            self.check_releases()
            files = server.get_files(self.project, self.package, self.release)
            print 'Found %s files in %s :'  % ( len(files), self.get_location())
            files.sort()
            for file in files:
                print '\t %s' %  file
        elif self.package:
            self.check_packages()
            releases = server.get_releases(self.project, self.package)
            print 'Found %s releases in %s/%s :'  % ( len(releases), self.project, self.package)
            releases.sort()
            for release in releases:
                print '\t %s'  % release
        else:
            packages = server.get_packages(self.project)
            print 'Found %s packages in %s :'  % ( len(packages), self.project) 
            packages.sort()
            for package in packages:
                print '\t %s'  % package

    def get_location(self):
        return '%s/%s/%s' % (self.project, self.package, self.release)

    def add(self):
        """Create the missing elements and upload the files to the server.

        Use the check method to get the different elements exist on the server.
        Create the missing element and upload the files on the server.
        The files are listed in the path directory which is specify with the option ("-d", "--dir")


        >>> python gforge_upload -d /home/user add openalea:VPlants:0.8:*.egg
              Upload the files which exists in /home/user directory to /VPlants package
                                                                     /release 0.8
                                                                     /openalea project
                                                                     /on the gforge server
        """
        print green('Checking and connecting to the forge. Be patient')
        self.check_project()
        self.check_packages()
        self.check_releases()
        self.check_files()

        files = glob.glob(self.glob)
        if len(files)==0:
            print 'No file with glob %s found. Nothing to upload' % (self.glob)
            sys.exit(0)

        print purple('You are about to upload the following files on the gforge (in %s): ' % self.get_location())
        for f in files:	
            print '\t%s' %f

        for file in files:
            if os.path.basename(file) in self.server_files:
                print purple('%s already present on the gforge (in %s). It will therefore be replaced' %(os.path.basename(file), self.get_location()))
                if self.remove_file(file):
                    self.add_file(file)
            else:
                self.add_file(file)


    def remove(self):
        """Remove the elements (package/release/and files) on the server.

        Use the check method to get the different elements exist on the server.
        Remove the element listed on the server.

        >>> python gforge_upload remove openalea:VPlants:0.8:*.egg
            Remove all the '.egg' files of /VPlants package
                                           /release 0.8
                                           /openalea project
                                           /on the gforge server

        """
        print 'Checking and connecting to the forge. Be patient'
        self.check_project()
        self.check_packages()
        # if only --package is provided, we assume that the whole package must be deleted included all the files
        # if the --package and --release are provided, we assume that the release of this package must be deleted included the files
        # if the --package and --release and --glob are provided, we assume that files of project/package/release must be deleted
        if self.package and self.glob and self.release:
            self.check_releases()
            files = server.get_files(self.project, self.package, self.release)
            if len(files)==0:
                print 'No file with glob % found. Nothing to upload' % (self.glob)
                sys.exit(0)
            for file in files:
                if fnmatch(file, self.glob):
                    self.remove_file(file)
                else:
                    print '%s does not match the glob option %s. Skipped' % (file, self.glob)


        elif self.package and self.release and not self.glob:
            self.check_releases()
            files = server.get_files(self.project, self.package, self.release)
            print purple('You are about to delete the release %s that contains the following files: ' % self.get_location())
            for f in files:	
                print '\t%s' %f
            if self.ask(purple('Shall we proceed ?')):
                if self.dry_run:
                    pass
                else:
                    self.server.remove_release(self.project, self.package, self.release)
                print 'Release %s deleted' % self.release
            else:
                print 'skipped'

        elif self.package and not self.release and not self.glob:
            releases = server.get_releases(self.project, self.package)
            if len(releases)==0:
                if self.ask(purple('Shall we proceed in deleting empty package %s?' % self.package)):
                    if self.dry_run:
                        pass
                    else:
                        self.server.remove_package(self.project, self.package)
                else:
                    print 'skipped'

            for release in releases:
                files = server.get_files(self.project, self.package, release)
                print purple('You are about to delete the release %s that contains the following files: ' % release)
                for f in files:	
                    print '\t%s' %f

            if self.ask(purple('Shall we proceed ?')):
                if self.dry_run:
                    pass
                else:
                    self.server.remove_package(self.project, self.package)
                    print green('done')
            else:
                print 'skipped'

    def run(self):
        # Query the project/package/release
        if self.mode == 'query':
            self.query()
        # Add package and release on the server and upload files if any on the server
        elif self.mode == 'add':
            self.add()
        # Remove package/release/files from the server
        elif self.mode == 'remove' or self.mode == 'delete':
            self.remove()
        else:
            print 'Use --mode to provide a mode in %s. Type --help for more options ' % self.available_mode
            sys.exit(0)


def main():
    """This is the main parsing function to get user arguments

    """

    usage = """
    %prog query package information, create or remove package/release/project, 
    and add or remove files to the gforge.

    :Examples: 

    In order to test your command, use ther --dry-run option::

        %prog --dry-run --mode query --project openalea --package aml2py

    To add an egg file into the openalea web page into the VPlants package, 
    0.8 release, type::

        %prog --glob /home/user/*.egg --mode add --project openalea --package VPlants --release 0.8

    Similarly to remove a package::

        %prog --query remove --project openalea --package VPlants --release 0.8 --glob *.egg

    If a space is included within a name, use the \ to escape the space as follows or quotes::

        %prog --mode add --project vplants --release release\ 0.8 --project openalea --glob './*/dist/*egg'
"""

    parser = OptionParser(usage=usage)


    parser.add_option("-n", "--dry-run",
                      action='store_true', default=False,
                       help="don't actually do anything")
    parser.add_option("-l", "--login", dest='login', default= None,
        help="GForge login")
    parser.add_option("-p", "--password", dest='password', default= None,
        help="GForge password")
    parser.add_option("-Y", "--yes-to-all", dest='non_interactive', 
        default=False, action='store_true',
        help="answer yes to all questions (will overwrite existing file, delete requested files, create directory on the gforge if needed)")
    parser.add_option("-a", "--project", 
        help="specify the project e.g. openalea, vplants default is vplants")
    parser.add_option("-b", "--package", dest='package', default='openalea',
        help="specify the package section according to the GForge architecture")
    parser.add_option("-r", "--release", dest='release', default=None,
        help="specify therelease according to the GForge architecture")
    parser.add_option("-g", "--glob", dest='glob', default=None,
        help="glob for filenames to be uploaded")
    parser.add_option("-m", "--mode", dest='mode', default=None,
        help="mode in [add, query, remove]")

    try:
        (opts, args)= parser.parse_args()
    except Exception,e:
        parser.print_usage()
        print "Error while parsing args:", e
        raise e

    print bold("Running gforge_upload version %s" % __revision__.split()[2])
    if opts.non_interactive is True:
        print bold(red("You are running gforge_upload without interaction (-Y option)"))
        ok = raw_input(bold(red("We assume that you want to reply yes to all questions including file removal. Shall we continue ?")))
        if not ok:
            sys.exit(0)
 
    # Create the Uploader object
    uploader = Uploader(opts)
    uploader.run()



if __name__=='__main__' :
    main()








