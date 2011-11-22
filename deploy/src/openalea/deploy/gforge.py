# -*- python -*-
#
#       OpenAlea.Deploy: OpenAlea setuptools extension
#
#       Copyright 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

"""INRIA GForge SOAP python API wrappers (based on SOAPpy)

See test functions below 
The specification has been found on the web : http://gforge.inria.fr/soap

Creation of a soap server, which serve as proxy to redirect python function
and args into valid soap request and return results into Python.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

#import pkg_resources
#pkg_resources.require('soappy')

import os
from SOAPpy import SOAPProxy
import base64
import time
import getpass


class GForgeProxy(object):
    # URLs
    url = 'https://gforge.inria.fr:443/soap/index.php'
    urlwsdl = 'https://gforge.inria.fr/soap/index.php?wsdl'

    namespace = 'https://gforge.inria.fr'
    encoding = 'http://schemas.xmlsoap.org/soap/encoding/'

    def __init__(self):
        # SOAP proxy 
        self.server = SOAPProxy(self.url, namespace=self.namespace, 
                                encoding='ISO-8859-1') 

        #Uncomment the following lines for SOAP Debug informations
        #self.server.config.dumpSOAPOut = 1
        #self.server.config.dumpSOAPIn = 1

        # Global session id
        self.session = None
        self.userid = None
        self.passwd = None




    def login(self, userid=None, passwd=None):
        """  Open a session """

        if(userid is None):
            userid = raw_input("Enter your GForge login:")

        if(passwd is None):
            passwd = getpass.getpass("Enter you GForge password:")

        try:
            self.session = self.server.login(userid, passwd)
            self.userid = userid
            self.passwd = passwd

        except Exception,e :
            print e
        
            return self.session


    def logout(self):
        """ Close the session """
        self.server.logout(self.session)
        self.session = None


    def get_project_id(self, project_name):
        """ 
        Return the project id (formely the group_id) for a particular name
        Return -1 if failed
        """
        try:
            ret = self.server.getGroupsByName(self.session, [project_name])
            id = ret[0]['group_id'] 
            return id

        except Exception:
            return -1


    def get_project_details(self, project_id):
        """ 
        Return the project details in a dictionary
        @param project_id : a number or a name
        """
    
        project_id = self.convert_to_id(project_id)
        
        ret = self.server.getGroups(self.session, [project_id])
        id = ret[0]

        return id


    def get_packages(self, project_id):
        """ 
        Return a list of package name 
        @param project_id : a number or a name
        """

        (project_id,) = self.convert_to_id(project_id)
        pkgs = self.server.getPackages(self.session, project_id)
        return [ pkg['name'] for pkg in pkgs ]
                     

    def get_package_id(self, project_id, pkg_name):
        """ 
        Return the package id, -1 if failed 
        @param project_id : a number or a name
        """
        (project_id,) = self.convert_to_id(project_id)
        pkg_name = pkg_name.lower()

        try:
            pkgs = self.server.getPackages(self.session, project_id)

            for pkg in pkgs:
                if(pkg['name'].lower() == pkg_name):
                    return pkg['package_id']

        except:
            pass

        return -1


    def get_releases(self, project_id, package_id):
        """ 
        Return a list of release name 
        @param project_id : a number or a name
        @param package_id : a number or a name
        """
        project_id, package_id = self.convert_to_id(project_id, package_id)

        rels = self.server.getReleases(self.session, project_id, package_id)
        return [ rel['name'] for rel in rels ]


    def get_release_id(self, project_id, package_id, release_name):
        """ 
        Return the release id, -1 if failed 
        @param project_id : a number or a name
        @param package_id : a number or a name
        """
        release_name = release_name.lower()
        project_id, package_id = self.convert_to_id(project_id, package_id)

        try:
            releases = self.server.getReleases(self.session, project_id, package_id)

            for rel in releases:
                if(rel['name'].lower() == release_name):
                    return rel['release_id']
        except:
            pass

        return -1


    def get_release_details(self, project_id, package_id, release_id):
        """ 
        Return a tuple (name, date, notes, changes) 
        @param project_id : a number or a name
        @param package_id : a number or a name
        @param release_id : a number or a name
        """

        project_id, package_id, release_id = \
            self.convert_to_id(project_id, package_id, release_id)

        try:
            releases = self.server.getReleases(self.session, 
                                               project_id, package_id)

            for rel in releases:
                id = rel['release_id']

                if(id == release_id):
                    name = rel["name"]
                    date = rel["release_date"]
                    notes = rel["notes"]
                    changes = rel["changes"]

                    return (name, date, notes, changes)

        except Exception, e:
            print e
        
        return (None, None, None, None,)


    def get_files(self, project_id, package_id, release_id):
        """ 
        Return a list of package_name 
        @param project_id : a number or a name
        @param package_id : a number or a name
        @param release_id : a number or a name
        """

        project_id, package_id, release_id = \
            self.convert_to_id(project_id, package_id, release_id)

        files = self.server.getFiles(self.session, project_id, package_id, release_id)
        return [ f['name'] for f in files ]


    def get_file_id(self, project_id, package_id, release_id, file_name):
        """ 
        Return a file id 
        """

        file_name = file_name.lower()

        project_id, package_id, release_id = \
            self.convert_to_id(project_id, package_id, release_id)

        try:
            files = self.server.getFiles(self.session, project_id, package_id, release_id)

            for f in files:
                name = f['name']
                id = f['file_id']
            
                if(name.lower() == file_name):
                    return id

        except:
            pass

        return -1


    def get_file(self, project_id, package_id, release_id, file_id, filename=None):
        """ 
        Download a file given its id 
        If filename is not None, write file in filename
        Return the filename
        @param project_id : a number or a name
        @param package_id : a number or a name
        @param release_id : a number or a name
        @param file_id : a number or a name
        """

        project_id, package_id, release_id, file_id = \
            self.convert_to_id(project_id, package_id, release_id, file_id)


        if(not filename):
            files = self.server.getFiles(self.session, project_id, package_id, release_id)

            for f in files:
                name = f['name']
                id = f['file_id']
                if(id == file_id):
                    filename = name

        if(not filename):
            raise RuntimeError("Unknown file_id")

        filestr = self.server.getFile(self.session, project_id, package_id, release_id, file_id)

        # convert to binary structure
        binstr = base64.b64decode(filestr)

        # write file
        fhandle = open(filename, "wb")
        fhandle.write(binstr)
        fhandle.close()

        return filename


    
    def convert_to_id(self, project_id=None, package_id=None, 
                      release_id=None, file_id=None):
        """
        Utility function : Convert full names to id(s)
        Return an array containing id(s)
        @param project_id : a number or a name
        @param package_id : a number or a name
        @param release_id : a number or a name
        @param file_id : a number or a name
        """

        ret = []
        if(project_id and isinstance(project_id, str)):
            project_id = self.get_project_id(project_id)
            
        if(package_id and isinstance(package_id, str)):
            package_id = self.get_package_id(project_id, package_id)

        if(release_id and isinstance(release_id, str)):
            release_id = self.get_release_id(project_id, package_id, release_id)

        if(file_id and isinstance(file_id, str)):
            file_id = self.get_file_id(project_id, package_id, release_id, file_id)

        for id in project_id, package_id, release_id, file_id:
            if(not id): break
            ret.append(id)

        return ret


################################################################################
    def add_package(self, project_id, package_name, public=True):
        """ 
        Create a new package 
        @param project_id : a number or a name
        """
    
        (project_id,) = self.convert_to_id(project_id)
    
        try:
            return self.server.addPackage(self.session, 
                                          project_id, package_name, int(public))
        except Exception, e:
            print e


    def add_release(self, project_id, package_id, release_name, 
                    notes, changes):
        """ 
        Create a new release 
        @param project_id : a number or a name
        @param package_id : a number or a name
        """
    
        project_id, package_id = self.convert_to_id(project_id, package_id,)

        try:
            return self.server.addRelease(self.session, project_id, package_id, 
                                          release_name, notes, changes)
        except Exception, e:
            print e
        


    def add_big_file(self, project_id, package_id, release_id, filename, 
                 proc_type="any", file_type="other"):
        """ 
        Add a file in a particular release (for big file)
        @param project_id : a number or a name
        @param package_id : a number or a name
        @param release_id : a number or a name
        """

        project_id, package_id, release_id = \
            self.convert_to_id(project_id, package_id, release_id)

        name = os.path.basename(filename)

        # get type and processor
        type = type_id.get(file_type, type_id['other'])
        processor = proc_id.get(proc_type, proc_id['any'])

        print "Uploading %s..."%(name,)

        try:
            import gforge_util
            gforge_util.gforge_login(self.userid, self.passwd)
            gforge_util.upload_file(filename, project_id, package_id, release_id, type, processor)

            print "Done."
            
        except Exception, e:
            print e

    
    def add_file(self, project_id, package_id, release_id, filename, 
                 proc_type="any", file_type="other"):
        """ 
        Add a file in a particular release 
        @param project_id : a number or a name
        @param package_id : a number or a name
        @param release_id : a number or a name
        """

        _project_id, _package_id, _release_id = \
            self.convert_to_id(project_id, package_id, release_id)

        name = os.path.basename(filename)

        # convert file contents
        f = open(filename, "rb")
        binstr =  f.read()
        f.close()
        filestr = base64.b64encode(binstr)

        # get type and processor
        type = type_id.get(file_type, type_id['other'])
        processor = proc_id.get(proc_type, proc_id['any'])

        release_time = int(time.mktime(time.localtime()))

        print "Uploading %s..."%(name,),

        try:
            
            ret = self.server.addFile(self.session, _project_id, _package_id, _release_id,
                                 name, filestr, type, processor, release_time)
            print "Done."
            return ret
        
        except Exception, e:
            return self.add_big_file(project_id,package_id, release_id, 
                filename, proc_type, file_type)


    def remove_package(self, project_id, package_id):
        """
        Remove a package
        """

        project_id, package_id = \
            self.convert_to_id(project_id, package_id)

        import gforge_util
        gforge_util.gforge_login(self.userid, self.passwd)
        gforge_util.delete_package(project_id, package_id)



    def remove_release(self, project_id, package_id, release_id):
        """
        Remove a package
        """

        project_id, package_id, release_id = \
            self.convert_to_id(project_id, package_id, release_id)

        import gforge_util
        gforge_util.gforge_login(self.userid, self.passwd)
        gforge_util.delete_release(project_id, package_id, release_id)


    def remove_file(self, project_id, package_id, release_id, file_id):
        """remove a file"""
        project_id, package_id, release_id, file_id = \
            self.convert_to_id(project_id, package_id, release_id, file_id)
        
        import gforge_util
        gforge_util.gforge_login(self.userid, self.passwd)
        print 'Trying to delete file %s',
        gforge_util.delete_file(project_id, package_id, release_id, file_id)
        print 'Done.'



# CONST

proc_id = { "i386" : 1000,
            "ppc": 2000,
            "mips" : 3000,
            "sparc" : 4000,
            "ultrasparc": 5000,
            "ia64": 6000,
            "alpha" : 7000,
            "any" : 8000,
            "other" : 9999,
            }

               

              

type_id = { ".deb" : 1000,
            ".rpm": 2000,
            ".zip" : 3000,
            ".bz2" : 3100,
            ".gz" : 3110,
            "src .zip" : 5000,
            "src .bz2" : 5010,
            "src .gz" : 5020,
            "tar.gz" : 5020,
            "src .rpm" : 5100,
            "src other" : 5900,	
            ".jpg" : 8000,
            ".txt" : 8100,
            ".html" : 8200,
            ".pdf" : 8300,
            ".dmg" : 4000,
            ".pkg" : 4010,
            "other" : 9999,
            "Other" : 9999,

            }
            
            
				

################################################################################
import sys
if __name__ == "__main__" or "nose" in sys.argv[0]:

    def test_login():
        server = GForgeProxy()

        server.login()
        assert server.session
        server.logout()


    def test_project():
        server = GForgeProxy()

        id = server.get_project_id("openaleaa")
        assert id == -1

        id = server.get_project_id("openalea")

        assert id == 79
        details = server.get_project_details(id)
        assert details['homepage'] == 'openalea.gforge.inria.fr/dokuwiki'
        assert details['unix_group_name'] == 'openalea'

        details = server.get_project_details("openalea")
        assert details['homepage'] == 'openalea.gforge.inria.fr/dokuwiki'
        assert details['unix_group_name'] == 'openalea'


    def test_package():
        server = GForgeProxy()

        assert len(server.get_packages(79)) > 4
        assert server.get_packages(79) == server.get_packages("openalea")
        assert server.get_package_id(79, "openalea.deploy") == 1176

        assert server.get_package_id("openalea", "openalea.deploy") == \
            server.get_package_id(79, "openalea.deploy")
    
        
    def test_release():
        server = GForgeProxy()
            
        assert len(server.get_releases(79, 1176)) > 0
        assert server.get_releases(79, 1176) == server.get_releases("openalea", "openalea.deploy")
        
        assert server.get_release_id(79, 1176, "0.3" ) == 1304
        assert server.get_release_id(79, 1176, "0.3" ) == \
            server.get_release_id("openalea", "openalea.deploy", "0.3")

        assert server.get_release_details(79, 1176, 1304)[1] == 1185961860
        assert server.get_release_details(79, 1176, 1304) == \
            server.get_release_details("openalea", "openalea.deploy", "0.3")


    def test_file():
        server = GForgeProxy()

        assert len(server.get_files(79, 1176, 1304)) > 0
        assert server.get_files(79, 1176, 1304) == \
            server.get_files("openalea", "openalea.deploy", "0.3")
                                                 
        assert server.get_file_id(79, 1176, 1304, 'OpenAlea.Deploy-0.3.3.tar.gz') == 3698

        assert server.get_file_id(79, 1176, 1304, 'OpenAlea.Deploy-0.3.3.tar.gz') == \
            server.get_file_id("openalea", "openalea.deploy", "0.3", 'OpenAlea.Deploy-0.3.3.tar.gz')

        filename = server.get_file(79, 1176, 1304, 3698)
        assert server.get_file(79, 1176, 1304, 3698) == \
            server.get_file("openalea", "openalea.deploy", "0.3", 'OpenAlea.Deploy-0.3.3.tar.gz')

        assert filename

        import gzip
        f = gzip.GzipFile(filename)
        assert f
        assert f.read()
        f.close()
        os.remove(filename)


    def test_add_file():

        server = GForgeProxy()
        server.login()
        server.add_package("openalea", "test_pkg")
        assert server.get_package_id("openalea", "test_pkg") > 0

        server.add_release("openalea", "test_pkg", "0.1", "notes", "changes")
        assert server.get_release_id("openalea", "test_pkg", "0.1") > 0


        server.add_file("openalea", "test_pkg", "0.1", "./core.tgz", file_type="srcgz")
        assert server.get_file_id("openalea", "test_pkg", "0.1", "core.tgz") > 0

    def test_remove():    

        server = GForgeProxy()
        server.login()
        try:
            server.add_package("openalea", "test_pkg")
        except:
            pass

        try:
            server.add_release("openalea", "test_pkg", "test_release", "Test", "")
        except:
            pass


        assert server.get_release_id("openalea", "test_pkg", "test_release") > 0
        server.remove_release("openalea", "test_pkg", "test_release")
        server.remove_package("openalea", "test_pkg")

