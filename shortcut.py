################################################################################
# -*- python -*-
#
#       OpenAlea.DistX:   
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
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
                      StartIn = "", Icon = "", Description = ""):
    """ Create windows shortcut
    @param Name : link name
    @param Target : executable file path (ex : Pythonroot + pythonw.exe)
    @param Arguments : (ex python module path)
    @param StartIn : execution path (same as python module path)
    @param Icon : icon path (ex Pythonroot + '\\py.ico')
    @param Description : ...

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
   
    from win32com.shell import shell
    import win32api
    import pythoncom

    WinRoot = os.environ["windir"]
    Path = WinRoot    + "\\Profiles\\All Users\\Desktop\\%s.lnk"%(Name)
    Icon = (Icon, 0)
    
    # Get the shell interface.
    sh = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, None, \
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
 
    # Get an IPersist interface
    persist = sh.QueryInterface(pythoncom.IID_IPersistFile)
 
    # Set the data
    sh.SetPath(Target)
    sh.SetDescription(Description)
    sh.SetArguments(Arguments)
    sh.SetWorkingDirectory(StartIn)
    sh.SetIconLocation(Icon[0],Icon[1])
 
    # Save the link itself.
    persist.Save(Path, 1)

 
# if __name__ == "__main__":
# 	TempDir = os.environ["TEMP"]
 
# 	Name        =  "New Link"
# 	Target      =  Pythonroot + "pythonw.exe "
# 	Arguments   =  TempDir + "\\test.py"
# 	StartIn     =  TempDir
# 	Icon        =  Pythonroot + "\\py.ico"
# 	Description = "New Link"
 
# 	CreateWinShortCut(Path,Target,Arguments,StartIn,Icon,Description)



def CreateFDShortCut(Name, Exec, Version,
                       Icon = "", Description = ""):
    """ Create a desktop shortcut on freedesktop comptabile system
    @param Name : Shortcut name
    @param Exec : Command to execute
    @param Version
    @param Icon : Icon name
    @param Description : ...
    """

    if(not 'posix' in os.name): return


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
    --vendor="openalea" --add-category="OpenAlea"'%(deskfilename))

