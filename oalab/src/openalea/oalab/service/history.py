# Add header here

"""
Service to display history.
"""

__all__ = ['display_history', 'register_history_displayer']

__registry = []


class IHistoryDisplayer(object):
    def clear(self):
        """
        Empty the history
        """

    def append(self, txt):
        """
        Add a new line to the history
        :param txt: text to add into the current history
         :type txt: basestring
        """


def register_history_displayer(history_displayer):
    """
    An history_displayer is an object with a method "clear" and a method append (see IHistoryDisplayer interface) that display the history
    """
    __registry.append(history_displayer)


def display_history(history):
    """
    Add a new line *txt* of history in the displayers
    """
    for history_displayer in __registry:
        history_displayer.append(history)
