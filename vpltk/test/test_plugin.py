from openalea.vpltk import plugin

def test1():
    plugins = plugin.discover('wralea')
    assert 'openalea' in plugins
    
def test2():
    plugins = plugin.discover('wralea')
    myentrypoint = plugins['openalea']
    myplugin = plugin.Plugin(myentrypoint)
    assert myplugin.name == myentrypoint.name

