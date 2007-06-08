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

		
		# headerbitmapfile=open(os.path.join(self.bdist_dir,'header.bmp'),'wb')
		# b=zlib.decompress(base64.decodestring(HEADER_BITMAP))
		# headerbitmapfile.write(b)
		# headerbitmapfile.close()
		
		# setupicofile=open(os.path.join(self.bdist_dir,'setup.ico'),'wb')
		# b=zlib.decompress(base64.decodestring(SETUP_ICO))
		# setupicofile.write(b)
		# setupicofile.close()
		
		# wizardbitmapfile=open(os.path.join(self.bdist_dir,'wizard.bmp'),'wb')
		# b=zlib.decompress(base64.decodestring(WIZARD_BITMAP))
		# wizardbitmapfile.write(b)
		# wizardbitmapfile.close()

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
			_setwinreg.append('WriteRegStr %s `%s` `%s` `%s`\n'%(
				key, subkey, name, value))
			_unwinreg.append('DeleteRegKey %s `%s` `%s`\n'%(
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
;!insertmacro MUI_DEFAULT MUI_HEADERIMAGE_BITMAP "header.bmp"
;!insertmacro MUI_DEFAULT MUI_WELCOMEFINISHPAGE_BITMAP "wizard.bmp"
;!define MUI_HEADERIMAGE
!define MUI_ABORTWARNING
;!define MUI_ICON "setup.ico"
;!define MUI_UNICON "setup.ico"

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
!ifdef OPENALEA_LIB
Function CheckOpenAleaPath
@_get_openalea_dir@	
FunctionEnd

Function un.CheckOpenAleaPath
@_get_openalea_dir@
FunctionEnd
!endif

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
"""

SETUP_ICO="""\
"""

WIZARD_BITMAP="""\
"""



# --- EOF ---
