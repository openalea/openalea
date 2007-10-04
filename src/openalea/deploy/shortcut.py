################################################################################
# -*- python -*-
#
#       OpenAlea.Deploy : openalea setuptools extension
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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
################################################################################
 
__doc__ = """ Os Functions to add shortcut and Mime type association """

 
import os
import sys

def create_win_shortcut(name, target, arguments = "",
                        startin = "", icon = "", description = "",
                        menugroup = "OpenAlea"):
    
    """ Create windows shortcut
    @param name : link name
    @param target : executable file path (ex : Pythonroot + pythonw.exe)
    @param arguments : (ex python module path)
    @param startin : execution path (same as python module path)
    @param icon : icon path (ex Pythonroot + '\\py.ico')
    @param description : ...
    @param menugroup : Menu group entry

    ex :
    	TempDir = os.environ["TEMP"]
 
	Name        =  "New Link"
	Target      =  Pythonroot + "pythonw.exe "
	Arguments   =  TempDir + "\\test.py"
	StartIn     =  TempDir
	Icon        =  Pythonroot + "\\py.ico"
	Description = "New Link"
 
	CreateWinShortCut(Path,Target,Arguments,StartIn,Icon,Description)
    """

    (Name, Target, Arguments, StartIn, Icon, Description, MenuGroup) = \
           (name, target, arguments, startin, icon, description, menugroup)

    if((not 'win' in sys.platform) or (sys.platform == 'cygwin')):
        return
    
    try:
        from openalea.deploy import get_base_dir
        win32dir = get_base_dir('pywin32')
        os.environ['PATH'] += ';' + os.path.join(win32dir, 'pywin32_system32')
        from win32com.shell import shell, shellcon
    except Exception, e:
        print e
        print "ERROR : pywin32 is not installed. Cannot create shortcut."
        return
    
    import win32api
    import pythoncom

    MenuRoot = shell.SHGetFolderPath(0, shellcon.CSIDL_COMMON_PROGRAMS, 0, 0)
    MenuRoot = MenuRoot + "\\" + MenuGroup + "\\"
    
    if(not os.path.isdir(MenuRoot)):
        os.mkdir(MenuRoot)
    
    Path =   MenuRoot + "\\%s.lnk"%(Name)
    Icon = (Icon, 0) 
    
    # Get the shell interface.
    sh = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, \
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
 
    # Set the data
    sh.SetPath(Target)
    sh.SetDescription(Description)
    sh.SetArguments(Arguments)
    sh.SetWorkingDirectory(StartIn)
    if(Icon[0]):
        sh.SetIconLocation(Icon[0],Icon[1])
 
    # Save the link itself.
    sh.QueryInterface(pythoncom.IID_IPersistFile).Save(Path,0)
 

def set_win_reg(key, subkey, name, value):
    """
    Set windows registry
    """
       
    if((not 'win' in sys.platform) or (sys.platform == 'cygwin')):
        return

    try:
        import _winreg
      
    except ImportError, e:
        print "!!ERROR: Can not access to Windows registry."
        return

    keymap = { 'HKEY_CLASSES_ROOT': _winreg.HKEY_CLASSES_ROOT,
               'HKEY_CURRENT_CONFIG': _winreg.HKEY_CURRENT_CONFIG,
               'HKEY_CURRENT_USER': _winreg.HKEY_CURRENT_USER,
               'HKEY_DYN_DATA': _winreg.HKEY_DYN_DATA,
               'HKEY_LOCAL_MACHINE': _winreg.HKEY_LOCAL_MACHINE,
               'HKEY_PERFORMANCE_DATA': _winreg.HKEY_PERFORMANCE_DATA,
               'HKEY_USERS' :_winreg.HKEY_USERS,
               'HKCR': _winreg.HKEY_CLASSES_ROOT,
               'HKCC': _winreg.HKEY_CURRENT_CONFIG,
               'HKCU': _winreg.HKEY_CURRENT_USER,
               'HKDD': _winreg.HKEY_DYN_DATA,
               'HKLM': _winreg.HKEY_LOCAL_MACHINE,
               'HKPD': _winreg.HKEY_PERFORMANCE_DATA,
               'HKU' :_winreg.HKEY_USERS,                                  
               }

    if(name) : subkey += '/' + name
    try:
        _winreg.SetValue(keymap[key], subkey, _winreg.REG_SZ, value)
    except:
        print "Cannot set %s/%s/%s registery key"%(key, subkey, name)




def create_fd_shortcut(name, target, arguments = "", version="",
                       icon = "", description = "", menugroup="OpenAlea"):
    """ Create a desktop shortcut on freedesktop compatible system
    @param Name : Shortcut name
    @param Target : executable file path (ex : Pythonroot + pythonw.exe)
    @param Arguments : (ex python module path)
    @param Version
    @param Icon : Icon name
    @param Description : ...
    @param MenuGroup : category
    """

    (Name, Target, Arguments, Version, Icon, Description, MenuGroup) = \
               (name, target, arguments, version, icon, description, menugroup)
            
    if(not 'posix' in os.name): return

    Exec = "%s %s"%(Target, Arguments)

    # Generate .desktop file
    deskfilename = "%s.desktop"%(Name)
    deskfile = open(deskfilename, 'w')

    deskfile.write('[Desktop Entry]\n')
    deskfile.write('Version=%s\n'%(Version))
    deskfile.write('Type=Application\n')
    deskfile.write('Name=%s\n'%(Name))
    deskfile.write('Comment=%s\n'%(Description))
    deskfile.write('TryExec=%s\n'%(Exec))
    deskfile.write('Exec=%s %s\n'%(Exec, '%F'))
    deskfile.write('Icon=%s\n'%(Icon))
    #deskfile.write('MimeType=image/x-foo;\n')

    deskfile.close()

    os.system('desktop-file-install %s \
    --vendor="openalea" --add-category="%s"'%(deskfilename, MenuGroup))

