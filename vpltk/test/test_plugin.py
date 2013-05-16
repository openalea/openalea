from openalea.vpltk import plugin

def test1():
    plugins = plugin.discover('wralea')
    assert 'vpltk' in plugins
    
def test2():
    plugins = plugin.discover('wralea')
    myentrypoint = plugins['vpltk']
    myplugin = plugin.Plugin(myentrypoint)
    assert myplugin.name == myentrypoint.name

