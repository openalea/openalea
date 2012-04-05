###############################################################################
# -*- python -*-
#
#       OpenAlea.Deploy : OpenAlea setuptools extension
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
""" Environment variable manipulation functions """

__license__ = "Cecill-C"
__revision__ = " $Id$"

import os
import sys


def set_lsb_env(name, vars):
    """
    Write a sh script in /etc/profile.d which set some environment variable
    LIBRARY_PATH and PATH are processed in order to avoid overwriting

    :param name: file name string without extension
    :param vars: ['VAR1=VAL1', 'VAR2=VAL2', 'LIBRARY_PATH=SOMEPATH']
    """

    if(not 'posix' in os.name):
        return

    # Build string
    exportstr = "############ Configuration ############\n\n"

    for newvar in vars:

        vname, value = newvar.split('=')

        # Exception
        lib_names = ['LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LD_FRAMEWORK_PATH']
        if (vname in lib_names and
           (value == "/usr/local/lib") or
           (value == "/usr/lib")):
            continue

        if(((vname in lib_names) or (vname== "PATH")) and value):
            exportstr += 'if [ -z "$%s" ]; then\n'%(vname)
            exportstr += '  export %s=%s\n'%(vname, value, )
            exportstr += 'else\n'
            exportstr +='   export %s=%s:$%s\n'%(vname, value, vname, )
            exportstr += 'fi\n\n'

        elif(vname and value):
            exportstr += 'export %s=%s\n\n'%(vname, value)

    exportstr += "############ Configuration END ########"

    try:
        filename = '/etc/profile.d/'+name+'.sh'
        filehandle = open(filename, 'w')
    except:
        print "Warning : Cannot create /etc/profile.d/%s.sh"%(name)
        print "Trying to setup environment in the ~/.bashrc file"

        # If profile.d directory is not writable, try to update $HOM/.bashrc
        try:
            script_name = ".%s.sh"%(name)

            # On Mac, we set the /etc/profile file (there is not .bashrc file)	
            if "darwin" in sys.platform.lower():
                filename = os.path.join(os.path.expanduser('~'), ".profile")
            else:
                filename = os.path.join(os.path.expanduser('~'), ".bashrc")
            filehandle = open(filename, 'r')
            bashrc = filehandle.read()
            filehandle.close()

            # create the string to look for : "source ~/.openalea.sh"
            bashrc_cmd = "source ~/%s"%(script_name, )

            # post processing: remove all commented lines to avoid to consider
            # these lines as valid; in particular :"#source ~/.bashrc
            bashrc_list = bashrc.split('\n')
            bashrc = []
            for line in bashrc_list:
                if not line.startswith('#'):
                    bashrc.append(line)

            # search for the "source ~/.openalea.sh" string
            if not bashrc_cmd in bashrc:
                filehandle = open(filename, 'a+')
                filehandle.write('\n'+bashrc_cmd)
                filehandle.close()

            # create the openalea shell script
            filename = os.path.join(os.path.expanduser('~'), script_name)
            filehandle = open(filename, 'w')

        except Exception, e:
            print e
            raise

    print "Creating %s"%(filename, )

    filehandle.write(exportstr)

    filehandle.close()
    #cmdstr = "(echo $SHELL|grep bash>/dev/null)&&. %s
    #||source %s"%(filename,filename)
    cmdstr = ". %s"%(filename, )
    print "To enable new OpenAlea config, open a new shell or type"
    print '  $ %s' % (bashrc_cmd)


def set_win_env(vars):
    """
    Set Windows environment variable persistently by editing the registry

    :param vars: ['VAR1=VAL1', 'VAR2=VAL2', 'PATH=SOMEPATH']
    """

    if(not 'win32' in sys.platform):
        return

    for newvar in vars:

        from string import find
        try:
            import _winreg
        except ImportError, e:
            print "!!ERROR: Can not access to Windows registry."
            return

        def queryValue(qkey, qname):
            qvalue, type_id = _winreg.QueryValueEx(qkey, qname)
            return qvalue

        regpath = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
        reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
        try:
            key = _winreg.OpenKey(reg, regpath, 0, _winreg.KEY_ALL_ACCESS)
        except:
            regpath = r'Environment'
            reg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
            key = _winreg.OpenKey(reg, regpath, 0, _winreg.KEY_ALL_ACCESS)
            

        name, value = newvar.split('=')

        # Specific treatment for PATH variable
        if name.upper() == 'PATH':
            value = os.path.normpath(value)
            actualpath = queryValue(key, name)

            listpath = actualpath.split(';')
            if not (value in listpath):
                value = actualpath + ';' + value
                print "ADD %s to PATH" % (value, )
            else:
                value = actualpath

            # TEST SIZE
            if(len(value) >= 8191):
                print "!!ERROR!! : PATH variable cannot contain more than 8191 characters"
                print "!!ERROR!! : Please : remove unused value in your environement"
                value = actualpath

        if(name and value):

            expand = _winreg.REG_SZ
            # Expand variable if necessary
            if("%" in value):
                expand = _winreg.REG_EXPAND_SZ

            _winreg.SetValueEx(key, name, 0, expand, value)
            #os.environ[name] = value #not necessary

        _winreg.CloseKey(key)
        _winreg.CloseKey(reg)

    # Refresh Environment
    try:
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        sParam = "Environment"

        import win32gui
        res1, res2 = win32gui.SendMessageTimeout(HWND_BROADCAST,
            WM_SETTINGCHANGE, 0, sParam, SMTO_ABORTIFHUNG, 100)
        if not res1:
            print ("result %s, %s from SendMessageTimeout" % (bool(res1), res2))

    except Exception, e:
        print e

