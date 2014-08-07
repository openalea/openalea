"""
==============================
interface plugin documentation
==============================

Details
=======

.. autoclass:: openalea.oalab.plugins.interface.IPluginInterface
    :members: __call__, name

"""

class IPluginInterface(object):
    """
    group of interfaces
    """

    interfaces = [] # List of interface names

    def __call__(self):
        """
        return a list of interface classes
        """
