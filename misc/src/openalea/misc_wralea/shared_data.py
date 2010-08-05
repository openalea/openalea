from openalea.core import Node

class SharedDataBrowser(Node):
    """test

    """
    def __init__(self, packages, glob):
        Node.__init__(self, packages, glob)

    def __call__(self, inputs):
        return (self.output_filename2,)

 
