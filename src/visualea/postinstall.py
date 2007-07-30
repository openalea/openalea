# Postinstall scripts


def install():
    
    from openalea.deploy import create_win_shortcut, set_win_reg, create_fd_shortcut
    import sys
    
    create_win_shortcut(name = 'Visualea',
                        target = sys.executable,
                        arguments = pj(sys.prefix, 'Scripts', 'visualea.exe'),
                        startIn = "", 
                        icon = "",
                        description = "Visual programming",
                        menuGroup = "OpenAlea")
        

    create_fd_shortcut(name='Visualea',
                       target=sys.executable, 
                       arguments=pj(sys.prefix, 'bin', 'visualea'), 
                       group='OpenAlea', 
                       icon='' )
   


def uninstall():
    pass
