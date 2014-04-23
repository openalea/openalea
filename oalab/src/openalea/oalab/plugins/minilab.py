from openalea.vpltk.plugin import iter_plugins

config_template = """
# Configuration file for application.

c = get_config()

#------------------------------------------------------------------------------
# MainConfig configuration
#------------------------------------------------------------------------------

# This is an application.

# MainConfig will inherit config from: Application

# Set the log level by value or name.
# c.MainConfig.log_level = 30

# The Logging format template
# c.MainConfig.log_format = '[%(name)s]%(highlevel)s %(message)s'

# Load this config file
# c.MainConfig.config_file = u''

# The date format used by logging formatters for %(asctime)s
# c.MainConfig.log_datefmt = '%Y-%m-%d %H:%M:%S'

#------------------------------------------------------------------------------
# MainWindowConfig configuration
#------------------------------------------------------------------------------

# Display package manager
c.MainWindowConfig.packages = False

# Display control panel
c.MainWindowConfig.controlpanel = False

# Display Help widget
c.MainWindowConfig.helpwidget = True

# Display 3D Viewer
c.MainWindowConfig.viewer3d = False

# Display menu bar
c.MainWindowConfig.menu = True

# Display project tree view
c.MainWindowConfig.project = False

# Display graphical Python interpreter
c.MainWindowConfig.shell = True

# Display search widget for package manager
c.MainWindowConfig.packagesearch = False

# Display logger (usefull to debug)
c.MainWindowConfig.logger = False

# List of graphical Python interpreters, sorted by preference
c.MainWindowConfig.shell_priority = ['oalab:IPythonShell', 'oalab:BuiltinShell']

# Display alea_install_gui
c.MainWindowConfig.store = False

# Display package manager sorted by categories
c.MainWindowConfig.packagecategories = False"""

class OALabExtensionMini(object):

    data = {
        'extension_name': 'mini',
        'implements' : ['IOAExtension'],
        'config_template': config_template,
    }

    def __call__(self, mainwin):
        from openalea.core.path import path
        from openalea.core.settings import get_openalea_home_dir
        from openalea.oalab.config.main import MainConfig
        from openalea.oalab.config.template import config_file_mini

        config_manager = MainConfig()
        config_manager.initialize()

        filename = ('oalab_' + self.data['extension_name'] + '.py')
        conf = path(get_openalea_home_dir()) / filename
        if not conf.exists():
            with conf.open('w') as f:
                # TODO : auto generate config file
                # f.write(self._config.generate_config_file())
                f.write(self.data['config_template'])

        config_manager.load_config_file(filename=filename, path=get_openalea_home_dir())
        config = config_manager.config

        for widget_factory_class in iter_plugins('oalab.widget'):

            # Select appropriate widgets based on config

            identifier = widget_factory_class.data['name'].lower()
            display = config.get('MainWindowConfig').get(identifier.lower(), False)
            if display:
                widget_factory = widget_factory_class()
                widget_factory(mainwin)
