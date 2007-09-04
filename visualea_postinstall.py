# Postinstall scripts


def install():
    
    from openalea.deploy.shortcut import create_win_shortcut, set_win_reg, create_fd_shortcut
    import sys
    from os.path import join as pj

    winexe = sys.executable
    winexe = winexe.replace('python.exe', 'pythonw.exe')
        
    create_win_shortcut(name = 'Visualea',
                        target = winexe,
                        arguments = '"'+pj(sys.prefix, 'Scripts', 'visualea-script.pyw')+'"',
                        startin = "", 
                        icon = "",
                        description = "Visual programming",
                        menugroup = "OpenAlea")
        

    create_fd_shortcut(name='Visualea',
                       target=sys.executable, 
                       arguments=pj(sys.prefix, 'bin', 'visualea'), 
                       menugroup='OpenAlea', 
                       icon='' )
   


def uninstall():
    pass
