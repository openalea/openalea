from openalea.vpltk.plugin import iter_plugins

class OALabExtensionTissue(object):

    data = {
        'oalab': {
            'extensions': ['tissuelab'],
            },
        'implements' : ['IOAExtension']
    }

    def __call__(self, mainwin):
        for widget_factory_class in iter_plugins('oalab.widget'):
            widget_factory = widget_factory_class()
            print 'log', widget_factory_class.data
            widget_factory(mainwin)

