# Uninstall openalea, vplants and alinea in removing corresponding files
# main is "uninstall_all_windows()" function
# works only for windows


try:
    from path import path
except:
    from openalea.core.path import path

import os, sys
from platform import platform


def get_python_dir():
    return path(sys.prefix)/'Lib'/'site-packages'

def scripts_dir():
    return path(sys.prefix)/'Scripts'

def remove_packages(dirs):
    for f in dirs:
        if f.exists():
            if f.isdir():
                f.rmtree()
            else:
                f.remove()
        else:
            print "Can't remove %s" %f
            
def uninstall():
    if "windows" in platform().lower():
        uninstall_all_windows()
    else:
        print "Can't uninstall on an other OS that Windows"
                
def uninstall_all_windows():
    """ Try to remove all the openalea, Vplants and alinea packages
    """
    
    pp = get_python_dir() # python_path
    
    # remove egg-link
    oa = pp.glob('openalea*.egg-link')
    vp = pp.glob('vplants*.egg-link')
    al = pp.glob('alinea*.egg-link')
    remove_packages(oa+vp+al)
            
    # remove egg
    oa = pp.glob('openalea*.egg')
    vp = pp.glob('vplants*.egg')
    al = pp.glob('alinea*.egg')
    remove_packages(oa+vp+al)
        
    # remove shared_lib.pth
    pths = pp.glob('shared-lib.pth')
    if pths:
        if pths[0].exists():
            pths[0].remove()
        else:
            print "Can't remove %s" %pths[0]
    
    # Modify the easy_install.pth file
    pths = pp.glob('easy-install.pth')
    eapth = pths[0]
    
    f = eapth.open()
    easy = f.read()
    f.close()
    
    new_ea = []
    for l in easy.split('\n'):
        if 'openalea' in l.lower() or 'vplants' in l.lower():
            pass
        else:
            new_ea.append(l)
            
    s = '\n'.join(new_ea)
    f = eapth.open('w')
    f.write(s)
    f.close()
    
    # Uninstall scripts 
    # How to know what are the installed console scripts?
    scripts = scripts_dir()
    # remove alea
    l = scripts.glob('alea*')
    l+= scripts.glob('aml2py*')
    l+= scripts.glob('cpfg2lpy*')
    l+= scripts.glob('flowerdemo*')
    l+= scripts.glob('gforge*')
    l+= scripts.glob('lpy*')
    l+= scripts.glob('make_develop*')    
    l+= scripts.glob('phyllotaxis*')    
    l+= scripts.glob('upload_dist*')
    l+= scripts.glob('visualea*')
    l+= scripts.glob('vplab*')
    l+= scripts.glob('secondnature*')
    
    remove_packages(l)
        
    # Update Environment variable
    
    # Change PATH before changing OPENALEA_LIB
    # Remove the registery in the same spirit than environ_var in deploy...
    # TODO
    """
    import _winreg
    regpath = r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment'
    reg = _winreg.ConnectRegistry(None, _winreg.HKEY_LOCAL_MACHINE)
    key = _winreg.OpenKey(reg, regpath, 0, _winreg.KEY_ALL_ACCESS)
    libs = _winreg.QueryValueEx(key,'PATH')[0]
    libs = libs.split(';')
    
    new_libs = []
    
    for l in libs:
        if "%OPENALEA_LIB%" not in l:
            new_libs.append(l)
    
    set_win_env['PATH=%s'%new_libs]"""
    
    # Remove dirs in openalea_lib
    libs=os.environ['OPENALEA_LIB']
    libs = libs.split(';')
    # extract all the egg from OPENALEA_LIB
    eggs = [path(x.split('egg')[0]+'egg') for x in libs if 'egg' in x]
    
    remove_packages(eggs)
    
    sh_libs = [path(x) for x in libs if 'shared_libs' in x]
    remove_packages(sh_libs)

    libs = [path(x) for x in libs if 'egg' not in x and 'shared_libs' not in x]
    
    os.putenv('OPENALEA_LIB','')
    
