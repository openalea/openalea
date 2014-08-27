
from openalea.vpltk.plugin import iter_plugins, check_dependencies

class Applet(object):
    # TODO: become a manager ??
    _applets = {}

    @classmethod
    def register(cls, applet_name, applet):
        cls._applets[applet_name] = applet

    @classmethod
    def new(cls, name, klass, *args, **kwargs):
        if name in cls._applets:
            return cls._applets[name]
        else:
            applet = klass(*args, **kwargs)
            cls.register(name, applet)
            return applet


    @classmethod
    def instances(cls, **kwargs):
        return cls._applets.values()

    @classmethod
    def instance(cls, **kwargs):
        """
        This is a temporary service that will be replaced by more specialized service or
        services based on interface
        """
        if 'class_args' in kwargs:
            class_args = kwargs['class_args']
        else:
            class_args = {}

        instance = None
        err = 'Cannot find required applet'


        if 'identifier' in kwargs:
            identifier = kwargs['identifier']
            err = 'No applet named %s' % identifier
            if identifier in cls._applets:
                instance = cls._applets[identifier]
                return instance
            else:
                for plugin in iter_plugins('oalab.applet'):
                    if plugin.name == identifier:
                        if check_dependencies(plugin):
                            instance = plugin()
                            applet = instance(**class_args)
                            cls.register_applet(plugin.name, applet)
                            instance = cls._applets[identifier]
                            return instance
        raise NotImplementedError, err

get_applet = Applet.instance
get_applets = Applet.instances
register_applet = Applet.register
new_applet = Applet.new
