from openalea.vpltk.plugin import iter_plugins

class OALabExtensionTissue(object):

    data = {
        'extension_name': 'tissue',
        'implements' : ['IOAExtension']
    }

    def __call__(self, mainwin):
        for widget_factory_class in iter_plugins('oalab.widget'):

            # Select appropriate widget.
            # Currently, widget defines himself extensions it belong to.
            if self.data['extension_name'] in widget_factory_class.data['extensions']:
                widget_factory = widget_factory_class()
                widget_factory(mainwin)

