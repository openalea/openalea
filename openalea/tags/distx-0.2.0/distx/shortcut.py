################################################################################
# -*- python -*-
#
#       OpenAlea.DistX:   
#
#       Copyright or C or Copr. 2006 INRIA - CIRAD - INRA  
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

def CreateWinShortCut(Name, Target, Arguments = "",
                      StartIn = "", Icon = "", Description = "",
                      MenuGroup = "OpenAlea"):
    
    """ Create windows shortcut
    @param Name : link name
    @param Target : executable file path (ex : Pythonroot + pythonw.exe)
    @param Arguments : (ex python module path)
    @param StartIn : execution path (same as python module path)
    @param Icon : icon path (ex Pythonroot + '\\py.ico')
    @param Description : ...
    @param MenuGroup : Menu group entry

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
    

    if((not 'win' in sys.platform) or (sys.platform == 'cygwin')):
        return
    
    try:
        from win32com.shell import shell, shellcon
    except:
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
 


def CreateFDShortCut(Name, Target, Arguments = "", Version="",
                       Icon = "", Description = "", MenuGroup="OpenAlea"):
    """ Create a desktop shortcut on freedesktop comptabile system
    @param Name : Shortcut name
    @param Target : executable file path (ex : Pythonroot + pythonw.exe)
    @param Arguments : (ex python module path)
    @param Version
    @param Icon : Icon name
    @param Description : ...
    @param MenuGroup : category
    """

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

