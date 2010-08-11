from openalea.core import Node

class SharedDataBrowser(Node):
    """Browser of package share data directory.

    This node can be used either interactively or by connecting input nodes.

    If used interactively, double click on it and :
        #. select the pacakge you are interested in
        #. set up a glob pattern like '*' or '*.dat'
        #. the filename list should update itself and you can select the filename 
           you are interested in


    :return: the full pathname of the selected file.

    This iteractive browsing is useful for demonstration or simply to found and 
    identify data filenames.

    However, it can not be used for tests and demonstrations since you must select
    the package and filename manually. 

    In order to used the node in a non interactive way, you can connect an input
    node to the first connector related to set the package name (without the namespace)
    and a filename to the third connector.

    The first node can be either a list with one string or a string node.
    The second node must be a string node.

    See the tests in the VisuAlea package mananger in the directory OpenAlea/misc/test/ (e.g., 
    shared_data_browser and shared_data_browser_interactive)

    """
    def __init__(self, packages, glob):
        Node.__init__(self, packages, glob)
        self._output = None

    def __call__(self, inputs):
        package, glob, filename = inputs
        assert type(package) == list or type(package) == str

        # deal with particular case of user inputs (for demo usage, when no interaction with the widget is required)
        if package and  filename:
            if type(package)==list:
                cmd = 'from openalea.%s import get_shared_data' % package[0]
            elif type(package)==str:
                cmd = 'from openalea.%s import get_shared_data' % package
            exec(cmd)
            self._output = get_shared_data(filename)
            return (self._output,)
        else:
            return (self._output,)


