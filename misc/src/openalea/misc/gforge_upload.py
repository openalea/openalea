"""

OB
to do:
    argument should be 
        * filename (or directory)
        * package (string; id)
        * release
        * project
    if release or package is wrong, return list of valid package.

"""
# A script to upload all files within the OpenAlea WebSite : http://openalea.gforge.inria.fr


from optparse import OptionParser
from fnmatch import fnmatch

from openalea.core.path import path
from openalea.deploy.gforge import *


available_mode = ['query', 'add']
available_project = ['openalea', 'vplants', 'alinea']

server = GForgeProxy()

class UploadError(Exception):
    def __init__(self, msg):
        self.msg = msg

class Uploader(object):
    """TODO: Documentation

    """

    def __init__(self, project=None, package=None, release=None, filename=None, directory='.', simulate=True):
        
        self.project = project
        self.package = package
        self.release = release
        self.filename = filename
        self.directory = directory
        self.server = server
        self.simulate = simulate

    def __del__(self):
        """ Logout the session when this instance is deleted.
        """
        self.server.logout()

    
    def messages(self, elt, elements):
        """ Display the list of elements (e.g. package, release) which on the server.

        """
        elt.sort()
        msg = 'Packages in the '+elements+' :'
        underscore = '-'*len(msg)
        tab = '  '
        print msg
        print underscore
        print tab+('\n'+tab).join(elt)
    

    def check(self):
        """ Return the element (e.g. project, package) which exist on the server.
        
        Check if the different elements exist on the server. 
        Return a list of the element name which exists .
        """

        elts = []

        if self.project not in available_project: 
            print 'Error command : project must be either alinea, openalea or vplants'        
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
        

        return elts


    def query(self):
        """ 

        Query the project, package, release.
        
        """

        elements = self.check()
        n = len(elements)
        if n == 0:
            pass
        elif n==1:
            pkgs = self.server.get_packages(*elements)
            if pkgs:                
                self.messages(pkgs, elements[0])                    
        elif n==2:
            rels = self.server.get_releases(*elements)
            if rels:                
                self.messages(rels, elements[1])  
        elif n==3:
            fls = self.server.get_files(*elements)
            if fls:                
                self.messages(fls, elements[2])  
        '''
        else:
            files = server.get_files(self.project, self.package, self.release)
            print [f for f in files if fnmatch(f,self.filename)]
        '''

    
    def add(self):
        """Create the missing elements and upload the files to the server.

        """
        
        elements = self.check()
        n = len(elements)
        
        if n == 0:
            raise UploaderError('Please give an existing project.')

        assert n < 4
    
        # Add package and release on the server
        if n == 1 and self.package:
            print 'Add package %s'%self.package
            
            if not self.simulate:
                print 'Do you really add %s package'%self.package, 'in %s project'%self.project
                response = 'N'                
                response = raw_input("Y or N ? ")
                if response.lower() == 'y':
                    self.server.login() 
                    self.server.add_package(self.project, self.package)
                    print '%s package had been created on the server'%self.package
                else:
                    pass

        if self.release and (1 <= n <= 2):                    
            print 'Add release %s'%self.release
            
            if not self.simulate:
                print 'Do you really add %s release'%self.release, 'in %s package'%self.package
                response = 'N'                
                response = raw_input("Y or N ? ")
                if response.lower() == 'y':
                    self.server.login() 
                    self.server.add_release(self.project, self.package, self.release, 'notes', 'changes')
                    print '%s release had been created on the server'%self.release
                else:
                    pass 

        # Add files if any on the server
        if self.filename:
            # 1. get the files
            d = path(self.directory)
            print 'd', d
            files = d.files(self.filename)
            print 'files', files
                
            # 2. check if the files are not on the server
            server_files = server.get_files(self.project, self.package, self.release)
            files = [f for f in files if f.basename() not in server_files]

            outfiles = '\n'.join( [f for f in files if f.basename() in server_files])
            if outfiles:
                print 'Some files are on the server: %s'%outfiles

            # 3. add the files not in the server
            for f in files:
                print 'Upload file %s'%f.basename()
                if not self.simulate:
                    print 'Do you really upload %s file'%f.basename(), 'in %s release'%self.release
                    response = 'N'                
                    response = raw_input("[y|n]? ")
                    if response.lower() == 'y':
                        self.server.login() 
                        self.server.add_file(self.project, self.package, self.release, f)
                        print '%s file had been upload on the server'%f.basename()
                    else:
                        pass 
 
        return True


def main():
    """This is the main parsing function to get user arguments

    """

    usage = """
    %prog query package information, create new package/release/project, and add files to the gforge.
  
    %prog [options] query|add project:package:release:file
    or %prog [options] query|add project:package:release:pattern

    exemple: %prog --dry-run query openalea:aml2py
    %prog add openalea:VPlants:0.8:*.egg
"""
 
    parser = OptionParser(usage=usage)


    parser.add_option("-n", "--dry_run", 
                      action='store_true', default=False, 
                      dest='dry_run', help="don't actually do anything")

    parser.add_option("-d", "--dir", dest='directory', default= '.', 
        help="directory which contains the various files [default: %default]")

    
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

    
    # Create the Uploader object
    uploader = Uploader(**kwds)

    # Query the project/package/release 
    mode = args[0]

    if mode == 'query':    
        try:
            uploader.query()
        except UploadError, e:
            print e
            return opts

    # Add package and release on the server and upload files if any on the server
         
    elif mode == 'add':
        try:
            uploader.add()
        except UploadError, e:
            print e
            return opts

    return opts



if __name__=='__main__':
    main()
    

