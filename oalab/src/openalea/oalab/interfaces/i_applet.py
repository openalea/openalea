
from openalea.core.factory_decorator import inputs
from openalea.vpltk.catalog.interface import IInterface

class IApplet(IInterface):
    name = 'IApplet' # Unique identifier

    def __init__(self, session, controller, parent=None):
        """
        :param session: unique instance (kernel) managing configuration and plugins
        :param controller: instance that modify and manage data
        :param parent: parent widget, used by Qt for layout, memory management, ...
        """

    def actions(self):
        """
        Returns a list ["Tab name", [list of actions] ]
        Where "list of action" is a 3-item list : groupname(unicode), action(QAction), button_type(bool: 0 big button, 1 small button)

        Example::

            def actions(self):
                return self._actions = [["Python IDE","Text Edit", self.actionUndo,0],
                                        ["Python IDE","Text Edit", self.actionRedo,0]
                                       ]
        """
