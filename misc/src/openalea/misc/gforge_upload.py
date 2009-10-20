"""A script to Query package information, create new packages/releases, a
upload all files within the OpenAlea website: http://openalea.gforge.inria.fr


.. todo::
    * if package is not provided, guess it from the name ?
    * non interactif: remove all or not
    * add openalea:to*:0.1 -> bug warning: no create a to* package !!!
    * same for release....
    * use a function to uncomplicated the code

"""

__revision__ = " $Id: gforge_upload.py 1812 2009-09-10 moscardi $"

from optparse import OptionParser
from fnmatch import fnmatch

from openalea.core.path import path
from openalea.deploy.gforge import GForgeProxy, proc_id, type_id


available_mode = ['query', 'add', 'remove']
available_project = ['openalea', 'vplants', 'alinea']

server = GForgeProxy()


class UploaderError(Exception):
    def __init__(self, msg):
        self.msg = msg


class Uploader(object):
    """A script to Query package information, create new packages/releases, and
        upload all files within the OpenAlea website: http://openalea.gforge.inria.fr

    :Example:

    >>> python gforge_upload query openalea:aml2py
    >>> python gforge_upload -d /home/user add openalea:VPlants:0.8:*.egg
    >>> python gforge_upload remove openalea:VPlants:0.8:*.egg

    type --help to get more help and usage

    """
    def __init__(self, project=None, package=None, release=None, filename=None, directory='.', simulate=True, login=None, password=None):
        """Initialization of project/package/release and file names
        path of directory where the files exist
        simulation mode
        """
        self.project = project
        self.package = package
        self.release = release
        self.filename = filename
        self.directory = directory
        self.server = server
        self.simulate = simulate
        self.login = login
        self.password = password

    def __del__(self):
        """ Logout the session when this instance is deleted.

        """
        self.server.logout()

    def messages(self, elt, elements, element_name):
        """ Display the list of elements (e.g. package, release) which
        on the server.

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
        print question
        ok = raw_input("([y]/n)? ")
        return ok.lower() == 'y'


    def file_type(self, filename):
        """ Retrieve the file type

        :param filename: file's name
        Return the file type ('.zip'/'.gz'/'.other'...)

        """
        f = path.splitext(filename)
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

        if path(filename).fnmatch(win) or path(filename).fnmatch(linux):
            pt = 'i386'
        elif path(filename).fnmatch(python):
            pt = 'any'
        else:
            pt = 'other'
        return pt


    def check(self):
        """ Return the element (e.g. project, package) which exists on the
        server.

        Check if the different elements exist on the server.
        Return a list of the element name which exists.

        """
        elts = []
        self.server.login(self.login, self.password)

        if self.project not in available_project:
            print 'Error command : project must be either %s' % available_project
            return elts
        else:
            elts.append(self.project)

        # User do not give any package.
        if not self.package:
            return elts

        try:
            pkgs = server.get_packages(self.project)
        except:
            pkgs = []

        if self.package in pkgs:
            elts.append(self.package)
        else:
            return elts

        ###
        if not self.release:
            return elts

        try:
            releases = server.get_releases(self.project, self.package)
        except:
            releases = []

        if self.release in releases:
            elts.append(self.release)

        else:
            return elts

        ###
        
        if not self.filename:
            return elts

        try:
            files = server.get_files(self.project, self.package, self.release)
            fl = [f for f in files if path(f).fnmatch(self.filename)]
        except:
            files = []

        if len(fl) > 0 :
                elts.append(fl)

        else:
            return elts
        
        return elts


    def query(self):
        """ Query the project, package, release.

        Use the check method to get the different elements exist on the server.
        Display a list of the element name which exists


        >>> python gforge_upload query openalea:aml2py
            Display the list of releases which exists in /aml2py package
                                                        /openalea project
                                                        /on the gforge server
        """
        elements = self.check()
        n = len(elements)

        if n == 0:
            pass
        elif n==1: # project only
            pkgs = self.server.get_packages(*elements)
            if pkgs:
                self.messages(pkgs, '%s project' % elements[0], 'Packages')
        elif n==2: # project, package only
            rels = self.server.get_releases(*elements)
            if rels:
                self.messages(rels, '%s package' % elements[1], 'Releases')
        elif n==3: # project, package and release known
            fls = self.server.get_files(*elements)
            if fls:
                self.messages(fls, 'release %s' % elements[2], 'Files')
        elif n>=4:
            fls = elements[3:]
            if fls:
                for f in fls:
                    self.messages(f,'release %s' % elements[2], 'Files with pattern "%s"' % self.filename)
        '''
        else:
            files = server.get_files(self.project, self.package, self.release)
            print [f for f in files if fnmatch(f,self.filename)]
        '''


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

        elements = self.check()
        n = len(elements)

        if n == 0:
            raise UploaderError('Please give an existing project.')

        assert n < 4

        # Add package and release on the server
        if n == 1 and self.package and not self.release:
            if self.simulate:
                print 'Add %s package in %s project' % (self.package, self.project)
            else:
                msg = 'Do you really want to add %s package in %s project' % (self.package, self.project)

                if self.ask(msg):
                    self.server.add_package(self.project, self.package)
                    print '%s package has been created on the server' % self.package
                else:
                    return False

        if self.release and (1 <= n <= 2):
            if self.simulate:
                print 'Add release %s in %s package' % (self.release, p)
            else:
                msg = 'Do you really want to add release %s in %s package' % (self.release, self.package)

                if self.ask(msg):
                    self.server.add_release(self.project, self.package, self.release, 'notes', 'changes')
                    print 'release %s has been created on the server' % self.release
                else:
                    return False

        # Add files if any on the server
        if self.filename:
            # 1. get the files
            d = path(self.directory)
            files = d.files(self.filename)
            if not files:
                print 'No file named %s exists in %s'%(self.filename, d)

            # 2. check if the files are not on the server
            # There are files only if project, package, and release already existed.
            outfiles = []
            if n == 3:
                server_files = server.get_files(self.project, self.package, self.release)
                files = [f for f in files if f not in server_files]
                outfiles = '\n'.join( [f for f in files if f.basename() in server_files])
                if outfiles:
                    print 'Same files are already on the server: %s' % outfiles

            # 3. add the files not in the server
            for f in files:
                f_type = self.file_type(f)
                p_type = self.proc_type(f)

                if f in outfiles:
                    msg = 'Do you really want to update %s?'%f.basename()

                    if self.ask(msg):
                        print 'Upload file %s'%f.basename()
                        if not self.simulate:
                            self.server.remove_file(self.project, self.package, self.release, f.basename())
                        print 'the old %s file has been removed from the server'%f.basename()
                        if not self.simulate:
                            if path.getsize(f) > 2000000L:
                                self.server.add_big_file(self.project, self.package, self.release, f,
                                                            p_type, f_type)
                            else:
                                self.server.add_file(self.project, self.package, self.release, f,
                                                            p_type, f_type)
                        print 'the new %s file has been uploaded on the server'%f.basename()

                else:
                    msg = 'Do you really want to upload %s file in release %s'%(f.basename(), self.release)

                    if self.ask(msg):
                        if not self.simulate:

                            if path.getsize(f) > 2000000L:
                                self.server.add_big_file(self.project, self.package, self.release, f,
                                                            p_type, f_type)
                            else:
                                self.server.add_file(self.project, self.package, self.release, f,
                                                            p_type, f_type)
                        print '%s file has been uploaded on the server'%f.basename()

        return True

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
        elements = self.check()
        n = len(elements)
	
        if n == 1:
            if self.package:
                print 'Error Command : Check the Package'
                return False
            else:
                raise UploaderError('Impossible to remove a project.')

        assert n < 4

        # Remove package on the server

        if n == 2 and self.package:
            if self.release:
                print 'Error Command : Check the Release'
                return False
            else:           
                if self.simulate:
                    print 'Remove %s package from %s project'%(self.package, self.project)
                else:
                    msg = 'Do you really want to remove %s package from %s project?'%(self.package, self.project)

                    if self.ask(msg):
                        self.server.remove_package(self.project, self.package)
                        print '%s package has been removed from the server'%self.package
                    else:
                        return False
        

	# Remove package and release on the server
        
        if n == 3 and self.release and not self.filename:   
            if self.simulate:
                print 'Remove release %s from %s package'%(self.release, self.package)
            else:
                msg = 'Do you really want to remove release %s from %s package'%(self.release, self.package)

                if self.ask(msg):
                    self.server.remove_release(self.project, self.package, self.release)
                    print 'release %s has been removed from the server'%self.release
                else:
                    return False

        if self.filename:

            files = server.get_files(self.project, self.package, self.release)
            fl = [f for f in files if path(f).fnmatch(self.filename)]
            if len(fl)==0:
                print 'No file matches your filename. Check the spelling of the package and file'
            if len(fl) == len(files):
                msg = 'Do you want to remove all files from release %s?' % self.release

                if self.ask(msg):
                    msg = 'Do you really want to remove all files from release %s?' % self.release

                    if self.ask(msg):
                        for f in fl:
                            self.server.remove_file(self.project, self.package, self.release, f)
                            print '%s file has been removed from the server' % f

                        print 'All files have been remove from release %s' % self.release

            else:
                for f in fl:
                    if self.simulate:
                        print 'Remove %s file from %s release'%(f, self.release)
                    else:
                        msg = 'Do you really want to remove %s file from release %s?' % (f, self.release)

                        if self.ask(msg):
                            self.server.remove_file(self.project, self.package, self.release, f)
                            print '%s file has been removed from the server'%f


def main():
    """This is the main parsing function to get user arguments

    """

    usage = """
    %prog query package information, create or remove package/release/project, and add or remove files to the gforge.

    %prog [options] query|add|remove project:package:release:file or
    %prog [options] query|add|remove project:package:release:pattern

    exemple: %prog --dry-run query openalea:aml2py
    %prog -d /home/user add openalea:VPlants:0.8:*.egg
    %prog remove openalea:VPlants:0.8:*.egg
"""

    parser = OptionParser(usage=usage)


    parser.add_option("-n", "--dry-run",
                      action='store_true', default=False,
                      dest='dry_run', help="don't actually do anything")
    parser.add_option("-d", "--dir", dest='directory', default= '.',
        help="directory which contains the various files [default: %default]")
    parser.add_option("-l", "--login", dest='login', default= None,
        help="GForge login")
    parser.add_option("-p", "--password", dest='password', default= None,
        help="GForge password")



    try:
        (opts, args)= parser.parse_args()
    except Exception,e:
        parser.print_usage()
        print "Error while parsing args:", e
        raise e

    if (len(args) < 1 or args[0] not in available_mode):
        raise Exception("Incomplete command :specify command query or add")

    ################################################################

    # Get the params from the command line.
    project = release = package = filename = None

    if len(args) > 1:
        s = args[1]
        l = s.split(':')
        if len(l) > 4:
            raise 'Error'
        else:
            if len(l) >= 1:
                project = l[0]
            if len(l) >= 2:
                package = l[1]
            if len(l) >= 3:
                release = l[2]
            if len(l) >= 4:
                filename = l[3]

    kwds = {}
    kwds['project'] = project
    kwds['package'] = package
    kwds['release'] = release
    kwds['filename'] = filename
    kwds['directory'] = directory = opts.directory
    kwds['simulate'] = simulate = opts.dry_run
    kwds['login'] = opts.login
    kwds['password'] = opts.password

    # Create the Uploader object
    uploader = Uploader(**kwds)

    # Query the project/package/release
    mode = args[0]

    if mode == 'query':
        try:
            uploader.query()
        except UploaderError, e:
            print e
            return opts

    # Add package and release on the server and upload files if any on the server
    elif mode == 'add':
        try:
            uploader.add()
        except UploaderError, e:
            print e
            return opts

    # Remove package/release/files from the server
    elif mode == 'remove':
        try:
            uploader.remove()
        except UploaderError, e:
            print e
            return opts

    return opts


if __name__=='__main__' :
    main()








