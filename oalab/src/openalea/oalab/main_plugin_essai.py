# This is a temporary file to test Plugin System


DEBUG = True

def main():
    from openalea.oalab.plugins import PluginManager
    pluginManager = PluginManager()
    pluginManager.set_plugin_path('.\\plugins_dir')
    pluginManager.get_all_plugins()

    if DEBUG == True:
        for pl in pluginManager.plugins:
            print pl
            print '----'
            print pl.__name__
            print '----'
            print pl.__plugin_name__
            print '----'
            print pl.__categorie__
            print '----'
            print ''

    
if( __name__ == "__main__"):
    main()