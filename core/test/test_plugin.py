from openalea.core import plugin

def test1():
    plugins = plugin.discover('wralea')
    assert 'oalab' in plugins
    
def test2():
    plugins = plugin.discover('wralea')
    myentrypoint = plugins['oalab']
    myplugin = plugin.Plugin(myentrypoint)
    assert myplugin.name == myentrypoint.name

