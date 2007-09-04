# Postinstall scripts


def install():
    
    from openalea.deploy.shortcut import create_win_shortcut, set_win_reg, create_fd_shortcut
    import sys
    from os.path import join as pj

    winexe = sys.executable
    winexe = winexe.replace('python.exe', 'pythonw.exe')
    create_win_shortcut(name = 'OpenAlea Installer',
                        target = winexe,
                        arguments = '"'+pj(sys.prefix, 'Scripts', 'alea_install_gui-script.pyw')+'"',
                        startin = "", 
                        icon = "",
                        description = "OpenAlea Installation",
                        menugroup = "OpenAlea")
        

    
def uninstall():
    pass
