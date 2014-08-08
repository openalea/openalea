from openalea.core import Node

class SharedDataBrowser(Node):
    """This node permits to find a shared data file located in a given Python package.
    The data file is searched in the shared directories.
    
    It can be used either interactively or by connecting input nodes.

    To use it interactively, double click on it and :
        #. select the package you are interested in (e.g. 'openalea.stat_tool'),
        #. set a glob pattern (e.g. '*' or '*.dat') ; the filename list is then updated by itself,
        #. select the filename you are interested in.

    :return: the file path of the selected data file.

    This interactive browsing is useful for demonstration or simply to found and 
    identify data filenames.

    To use it non-interactively:
        #. set the package name by connecting a string node to the first connector,
        #. set the file name by connecting a string node to the third connector.

    See the tests in the VisuAlea package manager in the directory OpenAlea/misc/test/shared_data_browser

    """
    def __init__(self, package, glob):
        Node.__init__(self, package, glob)
        self._output = None

    def __call__(self, inputs):
        package, glob, filename = inputs
        if package and filename:
            m = __import__(package, fromlist=[''])
            from openalea.deploy.shared_data import get_shared_data_path
            self._output = get_shared_data_path(m.__path__, filename)
            return (self._output,)
        else:
            return (self._output,)


