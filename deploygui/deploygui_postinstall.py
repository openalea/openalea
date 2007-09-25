# Postinstall scripts


def install():
    
    from openalea.deploy.shortcut import create_win_shortcut, set_win_reg, create_fd_shortcut
    from openalea.deploy import get_base_dir
    import sys
    from os.path import join as pj

    # Get the location of the installed egg
    base_dir = get_base_dir('openalea.deploygui')
    share_dir = pj(base_dir, 'share')
    
    winexe = sys.executable
    winexe = winexe.replace('python.exe', 'pythonw.exe')
    create_win_shortcut(name = 'OpenAlea Installer',
                        target = winexe,
                        arguments = '"'+pj(sys.prefix, 'Scripts', 'alea_install_gui-script.pyw')+'"',
                        startin = "", 
                        icon = pj(share_dir, 'install_icon.ico'),
                        description = "OpenAlea Installation",
                        menugroup = "OpenAlea")
        

    
def uninstall():
    pass
