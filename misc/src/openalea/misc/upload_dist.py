"""

Authors: Thomas Cokelaer, Thomas.Cokelaer@sophia.inria.fr 

"""

__license__ = "Cecill-C"
__revision__ = " $Id: upload_dist.py 1662 2009-03-09 12:25:57Z cokelaer $"

import os
from optparse import OptionParser
import getpass
import glob
import warnings

from openalea.deploy.gforge import GForgeProxy


# if extension == "srcgz" --> type_id = "5020"
# else: type_id = "9999"
#  if(proc == "i386"):   proc = "1000"
# elif(proc == "any"):  proc = "8000"

class UploadDistributionToGForge(object):
    """
    
    >>> gforge = UploadDistributionToGForge(login='yourname', release='0.7')
    >>> gforge.upload_file('dist/file.egg')
    
    The name of the distribution file must be available in the list of packages
    that are posted on the gforge, which can be known using 
    
    >>> print gforge.packages
    
    
    
    
    todo: if release is not present on the gforge, create it.
    """
    def __init__(self, project='openalea', login=None, password=None, 
                 release=None, verbose=False):
        
        # initialisation weith user arguments
        self.gforge = GForgeProxy()
        self.login = login
        self.project = project
        self.password = password
        self.release = release
        self.verbose = verbose
        
        # post processing to be done only once since project is unique
        self.group_id = self.gforge.get_project_id(self.project)
        self.packages = self.gforge.get_packages(self.project)

        
        #others
        self.proc_type = 'any' 
        self.file_type = 'other'
        
        # initialised with get_package_id
        self.package = None        
        self.package_id = None
        
        # initialised once package is known
        self.release_id = None
        
        self.filename = None
        self.file_id = None

        # finally, some asserts
        self._check()
        
    def _check(self):
        """Sanity check"""
        assert type(self.release) == str
        assert type(self.login) == str
        assert type(self.project) == str
        
    def __str__(self):
        """ General information to be used by print function"""
        ustr = '>>>>>>>>>>>>>> Project information <<<<<<<<<<<<<\n'
        ustr += 'Project: %s with id %d\n' \
                    % (self.project, self.group_id)
        ustr += 'Current package: %s with id %s \n'\
            % (self.package, self.package_id)
        ustr += 'Release: %s with id %s \n'\
            % (self.release, self.release_id)
        ustr += 'current distribution to upload: %s with id %s \n\n'\
            % (self.filename, self.file_id)
        return ustr
            
    def func_login(self, login=None, password=None):
        """login into gforge"""
       
        if self.verbose:
            print 'Trying to log in...',
        if login and password:
            self.gforge.login(login, password)
        else:
            self.gforge.login(self.login, self.password)
        self.login = self.gforge.userid
        self.password = self.gforge.passwd
        if not self.gforge.session:
            self.error('Could not connect to the gforge. Check login and passwd')
        else:
            if self.verbose:
                print 'connection succeeded.' 
        
    def logout(self):
        self.gforge.logout()

    def error(self, msg):
        """Simple error message that also logout"""
        print "Logging out."
        self.logout()
        ValueError(msg)
        
    def get_package_id(self, package=None):
        """returns package id given project and package names"""
        if not package:
            package = self.package
        else:
            self.package = package
        self._check()
        if self.package in self.packages:
            self.package_id = self.gforge.get_package_id(self.project, package)
            if self.package_id == -1:
                self.error("Could not find id of packages %s. check name" 
                           % package)
        else:
            self.error("Package %s not in list of available package" % package)
        # now that the package is none, we can also check the release id
        self.release_id = \
            self.gforge.get_release_id(self.project, self.package, self.release)
    
        return self.package_id
    
    def get_release_id(self, package=None, release=None):
        """returns package id given project and package names"""
        if not release:
            release = self.release
        else:
            self.release = release
        self._check()
        self.get_package_id()
        return self.release_id
    
    def get_file_id(self, filename=None, package=None, release=None):
        """returns package id given project and package names"""
        """ check pacakge release"""
        if not filename:
            filename = self.filename
        else:
            self.filename = filename
        self._check()
        
        self.get_release_id()
        self.file_id = self.gforge.get_file_id(self.project, 
                                               self.package, 
                                               self.release, self.filename)
        return self.file_id
    
    def get_releases(self, package):
        """returns list of release given project and package names"""
        return self.gforge(self.project, package)
    
    def guess_package(self, filename):
        _package_map = {
                        'OpenAlea.SConsx':'OpenAlea.SConsX',
                        'OpenAlea.scheduler':'OpenAlea.scheduler',
                        }
        guess = os.path.basename(filename).split('-')[0]
        
        if guess in self.packages:
            if self.verbose:
                print 'Found %s in the list of official packages.continue...' \
                    % guess
        elif guess in _package_map.keys():
            if self.verbose:
                print 'Found % in the list package_map. Need to be fixed !!' \
                    % guess
            guess = _package_map[guess]
        elif guess.startswith('VPlants'):
            if self.verbose:
                print 'Found % in the list package_map. Need to be fixed !!' \
                    % guess
            guess = 'VPlants'
        else:
            self.error('Could not guess the package name (%) on the gforge' 
                       % guess)
            
        self.get_package_id(guess)
        return guess
    
    
    def delete_file(self, filename=None, package=None, release=None):
        """todo:check pacakge release"""
        
        print 'Removing the following file from the gforge:',
        print self.filename
        ret = raw_input('Do you want to delete and replace it  (yes/no)? ')
        if ret != 'yes':
            print 'File not uploaded. Logging out'
            self.logout()
            return
        else:
            self.gforge.remove_file(self.group_id, self.package_id, 
                                self.release_id, self.file_id)
        #update the file_id !!!!
        self.get_file_id()
    
    def upload_file(self, filename=None, package=None, 
                    user_release=None, verbose=False):
        """package must be in get_packages
        gforge.upload_file("filename.egg", "VPlants", "0.7")
        """
        # overwrite release if required
        if user_release:
            self.get_release_id(package, user_release)
            self.release = user_release # not great to overwrite the init...
        
        self._check()
            
        if package is None:
            self.guess_package(filename)
        else:
            pass
        
        # we just want the base name to get the id 
        self.filename = os.path.basename(filename)
        self.get_file_id()
        
        if verbose:
            print 'Uploading %s' % filename
            print self
            
        # file already present 
        if self.file_id != -1:
           warnings.warn("""
                File %s already present on the gforge
                """ % filename)
           self.delete_file(self.filename, self.package, self.release)
 
        # if deleted, the fild_id has been updated in delete_file and therefore
        # it is == to -1
        if self.file_id == -1:
        
            if self.verbose:
                print self.proc_type
                print self.file_type
            #here we use filename because we need the whole pathname
            self.gforge.add_file(self.project, self.package,
                                     self.release,
                                     filename,
                                     proc_type=self.proc_type,
                                     file_type=self.file_type)





def ParseParameters():
    """
    
    """

    usage = """Usage: %prog [options]

   

    """
    parser = OptionParser(usage=usage, \
        version = "%prog CVS $Id: upload_dist.py 1662 2009-03-09 12:25:57Z cokelaer $ \n" \
      + "$Name:  $\n")

    parser.add_option("-l", "--login", metavar='LOGIN',
        default=None, type='string', help="login name")
    
    parser.add_option("-p", "--password", metavar='PASSWORD',
        default=None, type='string', help="non encrypted password")

    parser.add_option("-v", "--verbose", 
        action="store_true",  default=False, help="verbose option")
    
    parser.add_option("-f", "--filename", 
        default=None, help="name of the file to upload, provided that it matches\
         one of the URLmap that is hardcoded")

    parser.add_option("-d", "--directory", 
        default='dist', help="directory with files to upload.")
 
    parser.add_option("-r", "--release", 
        default=None, help="release version")
  
    parser.add_option("-P", "--project", 
        default='openalea', help="project name. should be openalea.")
 
    (_opts, _args) = parser.parse_args()     
    return _opts, _args


def main():

    (opts, _args) = ParseParameters()
    if not opts.release:
        raise ValueError('--release is compulsory')
    
    # initialisation
    gforge = UploadDistributionToGForge(opts.project,  login=opts.login, 
                             password=opts.password, release=opts.release,
                             verbose=opts.verbose)
    gforge.func_login()
        
    if not opts.filename:
        pattern = opts.directory + os.sep + '*'
        for ufile in glob.glob(pattern):
            gforge.upload_file(ufile, verbose=opts.verbose)
        
    else:
        gforge.upload_file(opts.filename, verbose=opts.verbose)
        
    gforge.logout()
        
if (__name__=="__main__"):
    main()        