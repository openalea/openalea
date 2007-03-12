#License = Python Software Foundation License
#From http://sourceforge.net/projects/bdist-nsi/"




"""distutils.command.bdist_nsi

Implements the Distutils 'bdist_nsi' command: create a windows installer
exe-program."""

# created 2005/05/24, j-cg , inspired by the bdist_wininst of the python distribution

#these are the first pre-alpha releases for testing purpose only..

import sys, os, string, zlib, base64
from distutils.core import Command
from distutils.util import get_platform
from distutils.dir_util import create_tree, remove_tree
from distutils.errors import *
from distutils.spawn import spawn

class distx_bdist_nsi (Command):

	description = "create an executable installer for MS Windows"

	user_options = [('bdist-dir=', None,
						"temporary directory for creating the distribution"),
					('keep-temp', 'k',
						"keep the pseudo-installation tree around after " +
						"creating the distribution archive"),
					('target-version=', 'v',
						"require a specific python version" +
						" on the target system"),
					('no-target-compile', 'c',
						"do not compile .py to .pyc on the target system"),
					('no-target-optimize', 'o',
						"do not compile .py to .pyo (optimized)"
						"on the target system"),
					('dist-dir=', 'd',
						"directory to put final built distributions in"),
					('nsis-dir=', 'n',
						"directory of nsis compiler"),
                                        ('external-prefix=', None,
                                                "Prefix directory to install external data." ),
					]

	boolean_options = ['keep-temp', 'no-target-compile', 'no-target-optimize',
						'skip-build']

        
	def initialize_options (self):
		self.bdist_dir = None
		self.keep_temp = 0
		self.no_target_compile = 0
		self.no_target_optimize = 0
		self.target_version = None
		self.dist_dir = None
		self.nsis_dir = None
		self.bitmap = None
		self.title = None
		self.plat_name = None
		self.format = None
                self.external_prefix= None
                
	# initialize_options()


	def finalize_options (self):
		if self.bdist_dir is None:
			bdist_base = self.get_finalized_command('bdist').bdist_base
			self.bdist_dir = os.path.join(bdist_base, 'nsi')
		if not self.target_version:
			self.target_version = sys.winver
		if self.distribution.has_ext_modules():
			short_version = sys.version[:3]
			if self.target_version and self.target_version != short_version:
				raise DistutilsOptionError, \
						"target version can only be" + short_version
			self.target_version = short_version
		if self.nsis_dir is None:
			self.nsis_dir="c:\Program Files\NSIS"
		self.set_undefined_options('bdist',
					   ('dist_dir', 'dist_dir'),
                                           )

		cmdobj= self.distribution.get_command_obj('install_external_data')
                cmdobj.external_prefix= '_openalea'

		# Create dist 
		if( not os.path.isdir(self.dist_dir) ):
                     os.mkdir(self.dist_dir)
		

	# finalize_options()


	def run (self):
		if (sys.platform != "win32" and
		    (self.distribution.has_ext_modules()
		     or self.distribution.has_c_libraries())):

			raise DistutilsPlatformError (
				"This distribution contains extensions and/or C libraries;\
				must be compiled on a Windows 32 platform")
		
		
		self.run_command('build')

                # Get shortcut and var info
                shortcuts = self.distribution.win_shortcuts
                envvar = self.distribution.set_win_var
		winreg = self.distribution.winreg
                self.distribution.win_shortcuts = None
                self.distribution.set_win_var = None
		self.distribution.set_win_var = None
                
		install = self.reinitialize_command('install', reinit_subcommands=1)
		install.root = self.bdist_dir
		install.warn_dir = 0

		install.compile = 0
		install.optimize = 0
		
		for key in ('purelib', 'platlib', 'headers', 'scripts', 'data'):
			if key in ['purelib','platlib'] and sys.version > "2.2":
				value = '_python/Lib/site-packages'
			else:
				value = '_python'
			if key == 'headers':
				value = '_python/Include/$dist_name'
			if key == 'scripts':
				value = '_python/Scripts'
			setattr(install, 'install_' + key, value)
		self.announce("installing to %s" % self.bdist_dir)
		self.run_command('install')

		self.build_nsi(shortcuts, envvar, winreg)
		
		if not self.keep_temp:
			remove_tree(self.bdist_dir, self.verbose, self.dry_run)        

	# run()

	
	def build_nsi(self, shortcuts, envvar, winreg):
                """
                @param shortcut : list of Shortcut objects
                @param envvar : list of string (VAR=VALUE)
		@pram winreg : list (key, subkey, name, value)
                """

		_define = []
		if(not shortcuts): shortcuts = []
		if(not envvar): envvar = []
		if(not winreg): winreg = []

		if(len(shortcuts)) :
			_define.append('!define SHORTCUT\n')
		if(len(envvar)) :
			_define.append('!define ENVVAR\n')
		if(len(winreg)) :
			_define.append('!define WINREG\n')



		nsiscript = NSIDATA
		metadata = self.distribution.metadata
		lic=""
		for name in ["author", "author_email", "maintainer",
                     "maintainer_email", "description", "name", "url", "version"]:
			data = getattr(metadata, name, "")
			if data:
				lic = lic + ("\n    %s: %s" % (string.capitalize(name), data))
				nsiscript=nsiscript.replace('@'+name+'@',data)

		# License
		licensefile = filter(lambda x : os.path.exists(x),
				 ['license', 'license.txt',
				'license.TXT', 'LICENSE.TXT'])
		
		if licensefile:
			licensefile = licensefile[0]
			lic = lic + "\n\nLicense:\n" + open(licensefile,'r').read()

		if lic != "":
			lic="Infos:\n" +lic
			
			licfile=open(os.path.join(self.bdist_dir, 'license'),'wt')
			licfile.write(lic)
			licfile.close()
				
		distdir=os.path.join('..','..','..',self.dist_dir)
		if not os.path.exists(distdir):
			os.makedirs(distdir)

		# Target File name
		if self.target_version:
			installer_path = os.path.join(
				distdir,
				"%s.win32-py%s.exe" % (self.distribution.get_fullname(),
						       self.target_version))
		else:
			installer_path = os.path.join(
				distdir,
				"%s.win32.exe" % self.distribution.get_fullname())                
				
		nsiscript = nsiscript.replace('@installer_path@',installer_path)
		
		haspythonversion=";"
		if self.target_version.upper() not in ["","ANY"]:
			nsiscript=nsiscript.replace('@pythonversion@',self.target_version)
			haspythonversion=""
			
		nsiscript=nsiscript.replace('@haspythonversion@',haspythonversion)

		
		headerbitmapfile=open(os.path.join(self.bdist_dir,'header.bmp'),'wb')
		b=zlib.decompress(base64.decodestring(HEADER_BITMAP))
		headerbitmapfile.write(b)
		headerbitmapfile.close()
		
		setupicofile=open(os.path.join(self.bdist_dir,'setup.ico'),'wb')
		b=zlib.decompress(base64.decodestring(SETUP_ICO))
		setupicofile.write(b)
		setupicofile.close()
		
		wizardbitmapfile=open(os.path.join(self.bdist_dir,'wizard.bmp'),'wb')
		b=zlib.decompress(base64.decodestring(WIZARD_BITMAP))
		wizardbitmapfile.write(b)
		wizardbitmapfile.close()

		# OpenAlea dir for external data
		if(not self.external_prefix):
         		nsiscript=nsiscript.replace('@_get_openalea_dir@',
                                                    '    ClearErrors\n' + \
                                                    '    ReadEnvStr $OPENALEADIR "OPENALEADIR"\n' + \
	                                            '    IfErrors lbl_na\n' + \
	                                            '    Goto lbl_end\n' + \
	                                            '    lbl_na:\n'+ \
                                                    '    StrCpy $OPENALEADIR "c:\openalea"\n' +\
	                                            '    lbl_end:\n')
                else:
                        nsiscript=nsiscript.replace('@_get_openalea_dir@',
                                                    '    StrCpy $OPENALEADIR "%s"\n'%(self.external_prefix))
                
                # File NSIS template with file to install
		_f=[]
		_d=[]
		_fd=[]
		_fc=[]
		lastdir=""
		

		# Copy Python file
		files=[]
		directories=[]
		os.path.walk(self.bdist_dir+os.sep+'_python',self.visit,(files, directories, '_python'))
		if(len(files)) : _define.append('!define PYTHON_LIB\n')
		for each in files:
			if lastdir != each[0]:
				_f.append('  SetOutPath "$INSTDIR\%s"\n' % each[0])
				lastdir=each[0]
				if each[0] not in ['Lib\\site-packages','Scripts','Include','']:
					_d.insert(0,'    RMDir "$INSTDIR\\'+each[0]+'\"\n')
			_f.append('  File "_python\\'+each[1]+'\"\n')
			
			if (each[1][len(each[1])-3:].lower() == ".py"):
				_fc.append('"'+each[1]+'",\n')
				_fd.append('    Delete "$INSTDIR\\'+each[1]+'o'+'\"\n')
				_fd.append('    Delete "$INSTDIR\\'+each[1]+'c'+'\"\n')
			_fd.append('    Delete "$INSTDIR\\'+each[1]+'\"\n')
		

		# Copy OpenAlea files
		files=[]
		directories=[]
                os.path.walk(self.bdist_dir+os.sep+'_openalea',self.visit,(files, directories, '_openalea'))

		if(len(files)) : _define.append('!define OPENALEA_LIB\n')
		for each in files:
			if lastdir != each[0]:
				_f.append('  SetOutPath "$OPENALEADIR\%s"\n' % each[0])
				lastdir=each[0]
			_f.append('  File "_openalea\\'+each[1]+'\"\n')
			_fd.append('    Delete "$OPENALEADIR\\'+each[1]+'\"\n')

		directories.reverse()
		for each in directories:
                        _d.append('    RMDir "$OPENALEADIR\\'+each+'\"\n')
                _d.append('    RMDir "$OPENALEADIR "\n')
			
		nsiscript=nsiscript.replace('@_files@',''.join(_f))
		nsiscript=nsiscript.replace('@_deletefiles@',''.join(_fd))
		nsiscript=nsiscript.replace('@_deletedirs@',''.join(_d))

		
		# Python file compilation
		if (not self.no_target_compile) or (not self.no_target_optimize):
			bytecompilscript=BYTECOMPILE_DATA.replace('@py_files@',''.join(_fc))
			bytecompilfile=open(os.path.join(self.bdist_dir,'bytecompil.py'),'wt')
			bytecompilfile.write(bytecompilscript)
			bytecompilfile.close()
			
		
		if not self.no_target_compile:
			nsiscript=nsiscript.replace('@compile@','')
		else:
			nsiscript=nsiscript.replace('@compile@',';')		
			
		if not self.no_target_optimize:
			nsiscript=nsiscript.replace('@optimize@','')
		else:
			nsiscript=nsiscript.replace('@optimize@',';')

		# Start menu entry
		_shcut = []
		_unshcut = []
		for sh in shortcuts:
		    _shcut.append('    CreateDirectory "$SMPROGRAMS\%s"\n'%(sh.group))
		    _shcut.append('    CreateShortCut "$SMPROGRAMS\%s\%s.lnk" "%s" "%s" "%s" 0 "" "" "%s"\n'\
                        %(sh.group, sh.name, sh.target, sh.arguments, sh.icon, sh.description))
                    _unshcut.append('    Delete "$SMPROGRAMS\%s\%s.lnk"\n'%(sh.group, sh.name))
                    _unshcut.append('    RMDir "$SMPROGRAMS\%s"\n'%(sh.group,))
                                  
                nsiscript=nsiscript.replace('@_shortcut@',''.join(_shcut))
                nsiscript=nsiscript.replace('@_unshortcut@',''.join(_unshcut))
                                  
		# Environment variables
		_setenvvar = []
		_unenvvar = []
		for v in envvar:
                    name, value = v.split('=')
                    _setenvvar.append('Push "%s"\n'%(name))
                    _setenvvar.append('Push "%s"\n'%(value))
                    _setenvvar.append('Call AddToEnvVar\n')

                    _unenvvar.append('Push "%s"\n'%(name))
                    _unenvvar.append('Push "%s"\n'%(value))
                    _unenvvar.append('Call un.RemoveFromEnvVar\n')
            
		nsiscript=nsiscript.replace('@_setenvvar@',''.join(_setenvvar))
                nsiscript=nsiscript.replace('@_unenvvar@',''.join(_unenvvar))

		# Windows registery
		_setwinreg = []
		_unwinreg = []
		for (key, subkey, name, value) in winreg:
			_setwinreg.append('WriteRegStr %s "%s" "%s" "%s"\n'%(
				key, subkey, name, value))
			_unwinreg.append('DeleteRegKey %s "%s" "%s"\n'%(
				key, subkey, name))

		nsiscript=nsiscript.replace('@_setwinreg@',''.join(_setwinreg))
                nsiscript=nsiscript.replace('@_unwinreg@',''.join(_unwinreg))

		
                # Write a generate installer
		nsiscript=nsiscript.replace('@_define@',''.join(_define))
		nsifile=open(os.path.join(self.bdist_dir,'setup.nsi'),'wt')
		nsifile.write(nsiscript)
		nsifile.close()
		self.compile()
		
				
			
	def visit(self,arg,dir,fil):
                """ callback function in walk
                fill a list with relative file name
                @param arg : 3uples (output_files, output_directories, srcdir)
                """
                (output_files, output_directories,  srcdir) = arg
		for each in fil:
			if not os.path.isdir(dir + os.sep + each):
				f=str(dir + os.sep + each)[
					len(self.bdist_dir + os.sep + srcdir + os.sep):]
				
				output_files.append([os.path.dirname(f),f])
			else:
                                f=str(dir + os.sep + each)[
					len(self.bdist_dir + os.sep + srcdir + os.sep):]
				
                                output_directories.append(f)


				
				
	def compile(self):
		try:
			spawn([os.path.join(self.nsis_dir,'makensis.exe'),
			       os.path.join(self.bdist_dir,'setup.nsi')])
		except:
			print "Error: makensis executable not found, \
			add NSIS directory to the path or specify it with --nsis-dir"
			
				
					  
			
# class bdist_nsi

BYTECOMPILE_DATA="""\
from distutils.util import byte_compile
import sys
import os
d=os.path.dirname(sys.executable)
f=[@py_files@]
g=[]
for each in f:
	g.append(d+os.sep+each)
byte_compile(g, optimize=1, force=None,
					prefix=d, base_dir=None,
					verbose=1, dry_run=0,
					direct=1)
"""

NSIDATA="""\
!define PRODUCT_NAME "@name@"
!define PRODUCT_VERSION "@version@"
!define PRODUCT_PUBLISHER "@author@ <@author_email@>"
!define PRODUCT_WEB_SITE "@url@"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"
!define PRODUCT_STARTMENU_REGVAL "NSIS:StartMenuDir"
@_define@
!define ALL_USERS

Var "OPENALEADIR"

@haspythonversion@!define PRODUCT_PYTHONVERSION "@pythonversion@"
@compile@!define MISC_COMPILE "1"
@optimize@!define MISC_OPTIMIZE "1"

; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!insertmacro MUI_DEFAULT MUI_HEADERIMAGE_BITMAP "header.bmp"
!insertmacro MUI_DEFAULT MUI_WELCOMEFINISHPAGE_BITMAP "wizard.bmp"
!define MUI_HEADERIMAGE
!define MUI_ABORTWARNING
!define MUI_ICON "setup.ico"
!define MUI_UNICON "setup.ico"

; Language Selection Dialog Settings
!define MUI_LANGDLL_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_LANGDLL_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_LANGDLL_REGISTRY_VALUENAME "NSIS:Language"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "license"
; Components page
;!insertmacro MUI_PAGE_COMPONENTS
; Directory page
;!insertmacro MUI_PAGE_DIRECTORY
; Start menu page

!define MUI_STARTMENUPAGE_NODISABLE
!define MUI_STARTMENUPAGE_DEFAULTFOLDER ""
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${PRODUCT_UNINST_ROOT_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "${PRODUCT_UNINST_KEY}"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "${PRODUCT_STARTMENU_REGVAL}"
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
	!insertmacro MUI_LANGUAGE "English"
; MUI end ------


Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "@installer_path@"


InstallDir "C:\Python"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show



Function .onInit
;	!insertmacro MUI_LANGDLL_DISPLAY
	!ifdef PYTHON_LIB
	Call CheckPython
	!endif
	!ifdef OPENALEA_LIB
	Call CheckOpenAleaPath
	!endif
FunctionEnd

!ifdef PRODUCT_PYTHONVERSION
Function GetSpecificPythonPath
	Push $R0
	ClearErrors
	ReadRegStr $R0 HKLM "SOFTWARE\Python\PythonCore\${PRODUCT_PYTHONVERSION}\InstallPath" ""
	IfErrors lbl_na
	Goto lbl_end
	lbl_na:
	StrCpy $R0 ""
	lbl_end:
	Exch $R0
FunctionEnd
!else
Function GetPythonPath
	Push $R0
	Push $0
	Push $1
	StrCpy $0 0
	ClearErrors
	loop:
	EnumRegKey $R0 HKLM "SOFTWARE\Python\PythonCore" $0
	StrCmp $R0 "" lbl_end
	ReadRegStr $1 HKLM "SOFTWARE\Python\PythonCore\$R0\InstallPath" ""    
	StrCmp $1 "" lbl_end
	StrCpy $INSTDIR $1
	IntOp $0 $0 + 1
	Goto loop
	lbl_end:
	Pop $1
	Pop $0
	Pop $R0
FunctionEnd
!endif


Section "main" SEC01
	SectionIn 1 32 RO
	SetOverwrite ifnewer
	SetOutPath $INSTDIR
@_files@
	
	!ifdef MISC_COMPILE
	SetOutPath "$TEMP\_python\${PRODUCT_NAME}_${PRODUCT_VERSION}"
	File "bytecompil.py"
	nsExec::Exec '$INSTDIR\python.exe $TEMP\_python\${PRODUCT_NAME}_${PRODUCT_VERSION}\\bytecompil.py' $9
	!endif
	!ifdef MISC_OPTIMIZE
	SetOutPath "$TEMP\_python\${PRODUCT_NAME}_${PRODUCT_VERSION}"
	File "bytecompil.py"
	nsExec::Exec '$INSTDIR\python.exe -OO $TEMP\_python\${PRODUCT_NAME}_${PRODUCT_VERSION}\\bytecompil.py' $9
	!endif
	RMDir /r "$TEMP\_python\${PRODUCT_NAME}_${PRODUCT_VERSION}"
	RMDir "$TEMP\_python"
	
SectionEnd

; Optional section (can be disabled by the user)
!ifdef SHORTCUT
Section "Start Menu Shortcuts"
   SetShellVarContext all

@_shortcut@
  
SectionEnd
!endif

!ifdef ENVVAR
Section "Environment variables"
@_setenvvar@
SectionEnd
!endif

!ifdef WINREG
Section "Registery"
@_setwinreg@
SectionEnd
!endif


Function CheckPython
	!ifdef PRODUCT_PYTHONVERSION
	Push $9
	Call GetSpecificPythonPath
	Pop $9
	StrCmp $9 "" lbl_err lbl_ok
lbl_err:
	MessageBox MB_OK "Python ${PRODUCT_PYTHONVERSION} not found. Install it first."
	Abort
lbl_ok:
	StrCpy $INSTDIR $9
	!else
	Call GetPythonPath
	!endif
FunctionEnd

!ifdef PYTHON_LIB
Function .onVerifyInstDir
        
	IfFileExists $INSTDIR\python.exe goodpath
		Abort
	
	goodpath:
FunctionEnd
!endif

;Retrieve OpenAlea dir path
Function CheckOpenAleaPath
@_get_openalea_dir@	
FunctionEnd

Function un.CheckOpenAleaPath
@_get_openalea_dir@
FunctionEnd


Section -Post
  WriteUninstaller "$INSTDIR\${PRODUCT_NAME}_uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\${PRODUCT_NAME}_uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd

Section Uninstall
       SetShellVarContext all
       !ifdef OPENALEA_LIB
       Call un.CheckOpenAleaPath
       !endif
	
	Delete "$INSTDIR\${PRODUCT_NAME}_uninst.exe"
@_deletefiles@
@_deletedirs@
@_unshortcut@
@_unenvvar@
@_unwinreg@
	DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
	SetAutoClose true
SectionEnd

; Environment variable manipulation

!ifdef ENVVAR

!ifndef _AddToPath_nsh
!define _AddToPath_nsh
 
!verbose 3
!include "WinMessages.NSH"
!verbose 4
 
!ifndef WriteEnvStr_RegKey
  !ifdef ALL_USERS
    !define WriteEnvStr_RegKey \
       'HKLM "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"'
  !else
    !define WriteEnvStr_RegKey 'HKCU "Environment"'
  !endif
!endif


; AddToEnvVar - Adds the given value to the given environment var
;        Input - head of the stack $0 environement variable $1=value to add
;        Note - Win9x systems requires reboot
 
Function AddToEnvVar
 
  Exch $1 ; $1 has environment variable value
  Exch
  Exch $0 ; $0 has environment variable name
 
  DetailPrint "Adding $1 to $0"
  Push $2
  Push $3
  Push $4
 
 
  ReadEnvStr $2 $0
  Push "$2;"
  Push "$1;"
  Call StrStr
  Pop $3
  StrCmp $3 "" "" AddToEnvVar_done
 
  Push "$2;"
  Push "$1\\;"
  Call StrStr
  Pop $3
  StrCmp $3 "" "" AddToEnvVar_done
  
 
  Call IsNT
  Pop $2
  StrCmp $2 1 AddToEnvVar_NT
    ; Not on NT
    StrCpy $2 $WINDIR 2
    FileOpen $2 "$2\\autoexec.bat" a
    FileSeek $2 -1 END
    FileReadByte $2 $3
    IntCmp $3 26 0 +2 +2 
      FileSeek $2 -1 END 
    FileWrite $2 "$\\r$\\nSET $0=%$0%;$4$\\r$\\n"
    FileClose $2
    SetRebootFlag true
    Goto AddToEnvVar_done
 
  AddToEnvVar_NT:
    ReadRegStr $2 ${WriteEnvStr_RegKey} $0
    StrCpy $3 $2 1 -1 
    StrCmp $3 ";" 0 +2 
      StrCpy $2 $2 -1 
    StrCmp $2 "" AddToEnvVar_NTdoIt
      StrCpy $1 "$2;$1"
    AddToEnvVar_NTdoIt:
      WriteRegExpandStr ${WriteEnvStr_RegKey} $0 $1
      SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
 
  AddToEnvVar_done:
    Pop $4
    Pop $3
    Pop $2
    Pop $0
    Pop $1
 
FunctionEnd
 
; RemoveFromEnvVar - Remove a given value from a environment var
;     Input: head of the stack
 
Function un.RemoveFromEnvVar
 
  Exch $1 ; $1 has environment variable value
  Exch
  Exch $0 ; $0 has environment variable name
 
  DetailPrint "Removing $1 from $0"
  Push $2
  Push $3
  Push $4
  Push $5
  Push $6
  Push $7
 
  IntFmt $7 "%c" 26 # DOS EOF
 
  Call un.IsNT
  Pop $2
  StrCmp $2 1 unRemoveFromEnvVar_NT
    ; Not on NT
    StrCpy $2 $WINDIR 2
    FileOpen $2 "$2\autoexec.bat" r
    GetTempFileName $5
    FileOpen $3 $5 w
    GetFullPathName /SHORT $1 $1
    StrCpy $1 "SET $0=%$0%;$1"
    Goto unRemoveFromEnvVar_dosLoop
 
    unRemoveFromEnvVar_dosLoop:
      FileRead $2 $4
      StrCpy $6 $4 1 -1 # read last char
      StrCmp $6 $7 0 +2 # if DOS EOF
        StrCpy $4 $4 -1 # remove DOS EOF so we can compare
      StrCmp $4 "$1$\\r$\\n" unRemoveFromEnvVar_dosLoopRemoveLine
      StrCmp $4 "$1$\\n" unRemoveFromEnvVar_dosLoopRemoveLine
      StrCmp $4 "$1" unRemoveFromEnvVar_dosLoopRemoveLine
      StrCmp $4 "" unRemoveFromEnvVar_dosLoopEnd
      FileWrite $3 $4
      Goto unRemoveFromEnvVar_dosLoop
      unRemoveFromEnvVar_dosLoopRemoveLine:
        SetRebootFlag true
        Goto unRemoveFromEnvVar_dosLoop
 
    unRemoveFromEnvVar_dosLoopEnd:
      FileClose $3
      FileClose $2
      StrCpy $2 $WINDIR 2
      Delete "$2\\autoexec.bat"
      CopyFiles /SILENT $5 "$2\\autoexec.bat"
      Delete $5
      Goto unRemoveFromEnvVar_done
 
  unRemoveFromEnvVar_NT:
    ReadRegStr $2 ${WriteEnvStr_RegKey} $0
    StrCpy $6 $2 1 -1 # copy last char
    StrCmp $6 ";" +2 # if last char != ;
      StrCpy $2 "$2;" # append ;
    Push $2
    Push "$1;"
    Call un.StrStr ; Find `$1;` in $2
    Pop $3 ; pos of our dir
    StrCmp $3 "" unRemoveFromEnvVar_done
      ; else, it is in path
      # $1 - path to add
      # $2 - path var
      StrLen $4 "$1;"
      StrLen $5 $3
      StrCpy $6 $2 -$5 # $6 is now the part before the path to remove
      StrCpy $7 $3 "" $4 # $7 is now the part after the path to remove
      StrCpy $4 $6$7
 
      StrCpy $6 $4 1 -1 # copy last char
      StrCmp $6 ";" 0 +2 # if last char == ;
      StrCpy $4 $4 -1 # remove last char
 
      WriteRegExpandStr ${WriteEnvStr_RegKey} $0 $4
 
      ; delete reg value if null
      StrCmp $4 "" 0 +2 # if null delete reg
      DeleteRegValue ${WriteEnvStr_RegKey} $0
 
      SendMessage ${HWND_BROADCAST} ${WM_WININICHANGE} 0 "STR:Environment" /TIMEOUT=5000
 
  unRemoveFromEnvVar_done:
    Pop $7
    Pop $6
    Pop $5
    Pop $4
    Pop $3
    Pop $2
    Pop $1
    Pop $0
FunctionEnd
 
 
 
 
!ifndef IsNT_KiCHiK
!define IsNT_KiCHiK
 
###########################################
#            Utility Functions            #
###########################################
 
; IsNT
; no input
; output, top of the stack = 1 if NT or 0 if not
;
; Usage:
;   Call IsNT
;   Pop $R0
;  ($R0 at this point is 1 or 0)
 
!macro IsNT un
Function ${un}IsNT
  Push $0
  ReadRegStr $0 HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion
  StrCmp $0 "" 0 IsNT_yes
  ; we are not NT.
  Pop $0
  Push 0
  Return
 
  IsNT_yes:
    ; NT!!!
    Pop $0
    Push 1
FunctionEnd
!macroend
!insertmacro IsNT ""
!insertmacro IsNT "un."
 
!endif ; IsNT_KiCHiK
 
; StrStr
; input, top of stack = string to search for
;        top of stack-1 = string to search in
; output, top of stack (replaces with the portion of the string remaining)
; modifies no other variables.
;
; Usage:
;   Push "this is a long ass string"
;   Push "ass"
;   Call StrStr
;   Pop $R0
;  ($R0 at this point is "ass string")
 
!macro StrStr un
Function ${un}StrStr
Exch $R1 ; st=haystack,old$R1, $R1=needle
  Exch    ; st=old$R1,haystack
  Exch $R2 ; st=old$R1,old$R2, $R2=haystack
  Push $R3
  Push $R4
  Push $R5
  StrLen $R3 $R1
  StrCpy $R4 0
  ; $R1=needle
  ; $R2=haystack
  ; $R3=len(needle)
  ; $R4=cnt
  ; $R5=tmp
  loop:
    StrCpy $R5 $R2 $R3 $R4
    StrCmp $R5 $R1 done
    StrCmp $R5 "" done
    IntOp $R4 $R4 + 1
    Goto loop
done:
  StrCpy $R1 $R2 "" $R4
  Pop $R5
  Pop $R4
  Pop $R3
  Pop $R2
  Exch $R1
FunctionEnd
!macroend
!insertmacro StrStr ""
!insertmacro StrStr "un."
 
!endif ; _AddToPath_nsh
!endif ; ENVVAR
"""

HEADER_BITMAP="""\
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

"""
SETUP_ICO="""\
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
C9l/AGrOZTg=
"""

WIZARD_BITMAP="""\
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
j4mOPHbtxbVk7b8tsKtdb8zjfwFCxuEx

"""



# --- EOF ---
