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

__doc__ = """
INRIA GForge SOAP python API wrappers (based on SOAPpy)
See test functions below 
"""

import pkg_resources
pkg_resources.require('soappy')

import os, sys
from SOAPpy import SOAPProxy, WSDL
import base64
import time

# URLs
url = 'https://gforge.inria.fr:443/soap/index.php'
urlwsdl = 'https://gforge.inria.fr/soap/index.php?wsdl'

namespace = 'https://gforge.inria.fr'
encoding = 'http://schemas.xmlsoap.org/soap/encoding/'

# SOAP proxy 
server = SOAPProxy(url, namespace=namespace, encoding='ISO-8859-1') 

#Uncomment the following lines for SOAP Debug informations
#server.config.dumpSOAPOut = 1
#server.config.dumpSOAPIn = 1

# Global session id
session = None


import getpass

def login(userid=None, passwd=None):
    """  Open a session """
    global session, server

    if(userid is None):
        userid = raw_input("login:")

    if(passwd is None):
        passwd = getpass.getpass("password:")

    try:
        session = server.login(userid, passwd)
    except Exception,e :
        print e
        
    return session


def logout():
    """ Close the session """
    global session
    server.logout(session)
    session = None


def get_project_id(project_name):
    """ 
    Return the project id (formely the group_id) for a particular name
    Return -1 if failed
    """
    global session, server

    try:
        ret = server.getGroupsByName(session, [project_name])
        id = ret[0]['group_id'] 
        return id

    except Exception:
        return -1


def get_project_details(project_id):
    """ 
    Return the project details in a dictionary
    @param project_id : a number or a name
    """
    global session, server
    
    project_id = convert_to_id(project_id)

    ret = server.getGroups(session, [project_id])
    id = ret[0]

    return id


def get_packages(project_id):
    """ 
    Return a list of package name 
    @param project_id : a number or a name
    """
    global session, server

    (project_id,) = convert_to_id(project_id)
    pkgs = server.getPackages(session, project_id)
    return [ pkg['name'] for pkg in pkgs ]
                     

def get_package_id(project_id, pkg_name):
    """ 
    Return the package id, -1 if failed 
    @param project_id : a number or a name
    """
    global session, server
    (project_id,) = convert_to_id(project_id)

    pkg_name = pkg_name.lower()

    try:
        pkgs = server.getPackages(session, project_id)

        for pkg in pkgs:
            name = pkg['name'].lower()
            id = pkg['package_id']
        
            if(name.lower() == pkg_name):
                return id

        return -1

    except:
        return -1


def get_releases(project_id, package_id):
    """ 
    Return a list of release name 
    @param project_id : a number or a name
    @param package_id : a number or a name
    """
    global session, server
    project_id, package_id = convert_to_id(project_id, package_id)

    rels = server.getReleases(session, project_id, package_id)
    return [ rel['name'] for rel in rels ]


def get_release_id(project_id, package_id, release_name):
    """ 
    Return the release id, -1 if failed 
    @param project_id : a number or a name
    @param package_id : a number or a name
    """
    global session, server
    release_name = release_name.lower()
    
    project_id, package_id = convert_to_id(project_id, package_id)

    try:
        releases = server.getReleases(session, project_id, package_id)

        for rel in releases:
            name = rel['name'].lower()
            id = rel['release_id']
        
            if(name.lower() == release_name):
                return id

        return -1

    except:
        return -1


def get_release_details(project_id, package_id, release_id):
    """ 
    Return a tuple (name, date, notes, changes) 
    @param project_id : a number or a name
    @param package_id : a number or a name
    @param release_id : a number or a name
    """
    global session, server

    project_id, package_id, release_id = convert_to_id(project_id, package_id, release_id)

    try:
        releases = server.getReleases(session, project_id, package_id)

        for rel in releases:
            id = rel['release_id']

            if(id == release_id):
                name = rel["name"]
                date = rel["release_date"]
                notes = rel["notes"]
                changes = rel["changes"]

                return (name, date, notes, changes)

        return (None, None, None, None,)

    except Exception, e:
        print e
        return (None, None, None, None,)


def get_files(project_id, package_id, release_id):
    """ 
    Return a list of package_name 
    @param project_id : a number or a name
    @param package_id : a number or a name
    @param release_id : a number or a name
    """
    global session, server

    project_id, package_id, release_id = convert_to_id(project_id, package_id, release_id)

    files = server.getFiles(session, project_id, package_id, release_id)
    return [ f['name'] for f in files ]


def get_file_id(project_id, package_id, release_id, file_name):
    """ 
    Return a file id 
    """

    global session, server
    file_name = file_name.lower()

    project_id, package_id, release_id = convert_to_id(project_id, package_id, release_id)

    try:
        files = server.getFiles(session, project_id, package_id, release_id)

        for f in files:
            name = f['name'].lower()
            id = f['file_id']
            
            if(name.lower() == file_name):
                return id

        return -1

    except:
        return -1


def get_file(project_id, package_id, release_id, file_id, filename=None):
    """ 
    Download a file given its id 
    If filename is not None, write file in filename
    Return the filename
    @param project_id : a number or a name
    @param package_id : a number or a name
    @param release_id : a number or a name
    @param file_id : a number or a name
    """
    global session, server

    project_id, package_id, release_id, file_id = convert_to_id(project_id, package_id, 
                                                                release_id, file_id)


    if(not filename):
        files = server.getFiles(session, project_id, package_id, release_id)
        for f in files:
            name = f['name']
            id = f['file_id']
            if(id == file_id):
                filename = name

    if(not filename):
        raise RuntimeError("Unknown file_id")

    filestr = server.getFile(session, project_id, package_id, release_id, file_id)

    # convert to binary structure
    binstr = base64.b64decode(filestr)

    # write file
    fhandle = open(filename, "wb")
    fhandle.write(binstr)
    fhandle.close()

    return filename


    
def convert_to_id(project_id=None, package_id=None, release_id=None, file_id=None):
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
        project_id = get_project_id(project_id)

    if(package_id and isinstance(package_id, str)):
        package_id = get_package_id(project_id, package_id)

    if(release_id and isinstance(release_id, str)):
        release_id = get_release_id(project_id, package_id, release_id)

    if(file_id and isinstance(file_id, str)):
        file_id = get_file_id(project_id, package_id, release_id, file_id)

    for id in project_id, package_id, release_id, file_id:
        if(not id): break
        ret.append(id)

    return ret


################################################################################
def add_package(project_id, package_name, public=True):
    """ 
    Create a new package 
    @param project_id : a number or a name
    """
    
    global session, server
    
    (project_id,) = convert_to_id(project_id)
    
    try:
        server.addPackage(session, project_id, package_name, int(public))
    except Exception, e:
        print e


def add_release(project_id, package_id, release_name, notes, changes):
    """ 
    Create a new release 
    @param project_id : a number or a name
    @param package_id : a number or a name
    """
    
    global session, server

    project_id, package_id = convert_to_id(project_id, package_id,)

    try:
        server.addRelease(session, project_id, package_id, release_name, notes, changes)
    except Exception, e:
        print e
        


def add_file(project_id, package_id, release_id, filename, 
             proc_type="any", file_type="other"):
    """ 
    Add a file in a particular release 
    @param project_id : a number or a name
    @param package_id : a number or a name
    @param release_id : a number or a name
    """
    global session, server

    project_id, package_id, release_id = convert_to_id(project_id, package_id, release_id)

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

    print "Uploading %s..."%(name,)

    try:
        server.addFile(session, project_id, package_id, release_id,
                       name, filestr, type, processor, release_time)
        print "Done."
    except Exception, e:
        print e



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
            "src .rpm" : 5100,
            "src other" : 5900,	
            ".jpg" : 8000,
            ".txt" : 8100,
            ".html" : 8200,
            ".pdf" : 8300,
            ".dmg" : 4000,
            ".pkg" : 4010,
            "other" : 9999,
            }
            
            
				

################################################################################
def test_login():
    login()
    assert session
    logout()


def test_project():

    id = get_project_id("openaleaa")
    assert id == -1

    id = get_project_id("openalea")

    assert id == 79
    details =  get_project_details(id)
    assert details['homepage'] == 'openalea.gforge.inria.fr/dokuwiki'
    assert details['unix_group_name'] == 'openalea'

    details =  get_project_details("openalea")
    assert details['homepage'] == 'openalea.gforge.inria.fr/dokuwiki'
    assert details['unix_group_name'] == 'openalea'



def test_package():
    
    assert len(get_packages(79)) > 4
    assert get_packages(79) == get_packages("openalea")
    assert get_package_id(79, "openalea.deploy") == 1176

    assert get_package_id("openalea", "openalea.deploy") == \
        get_package_id(79, "openalea.deploy")
    

def test_release():
    
    assert len(get_releases(79, 1176)) > 0
    assert get_releases(79, 1176) == get_releases("openalea", "openalea.deploy")

    assert get_release_id(79, 1176, "0.3" ) == 1304
    assert get_release_id(79, 1176, "0.3" ) == \
        get_release_id("openalea", "openalea.deploy", "0.3")

    assert get_release_details(79, 1176, 1304)[1] == 1185961860
    assert get_release_details(79, 1176, 1304) == \
        get_release_details("openalea", "openalea.deploy", "0.3")


def test_file():

    assert len(get_files(79, 1176, 1304)) == 18
    assert get_files(79, 1176, 1304) == get_files("openalea", "openalea.deploy", "0.3")
                                                 
    assert get_file_id(79, 1176, 1304, 'OpenAlea.Deploy-0.3.3.tar.gz') == 3698

    assert get_file_id(79, 1176, 1304, 'OpenAlea.Deploy-0.3.3.tar.gz') == \
        get_file_id("openalea", "openalea.deploy", "0.3", 'OpenAlea.Deploy-0.3.3.tar.gz')

    filename = get_file(79, 1176, 1304, 3698)
    assert get_file(79, 1176, 1304, 3698) == \
        get_file("openalea", "openalea.deploy", "0.3", 'OpenAlea.Deploy-0.3.3.tar.gz')

    assert filename

    import gzip
    f = gzip.GzipFile(filename)
    assert f
    assert f.read()
    f.close()
    os.remove(filename)


def test_add_pkg():

    if(not session) : login()
    add_package("openalea", "test_pkg")
    assert get_package_id("openalea", "test_pkg") > 0


def test_add_release():

    if(not session) : login()
    add_release("openalea", "test_pkg", "0.1", "notes", "changes")
    assert get_release_id("openalea", "test_pkg", "0.1") > 0


def test_add_file():

    if(not session) : login()
    add_file("openalea", "test_pkg", "0.1", "./core.tgz", file_type="srcgz")
    assert get_file_id("openalea", "test_pkg", "0.1", "core.tgz") > 0

