# Add header here

"""
Service to display help.
"""

__all__ = ['help', 'register_helper']

__registry = []


class IHelper(object):
    def set_text(self, text):
        """
        :param text: text to display
        :type text: basestring
        """

def register_helper(helper):
    """
    An helper is an object with a method "set_text" (see IHelper interface)
    """
    __registry.append(helper)


def display_help(obj):
    """
    Displays help in all registered helpers.
    """
    doc = str(get_doc(obj))

    for helper in __registry:
        helper.set_text(doc)


def get_doc(obj):
    """
    Return documentation for given object
    :rtype: basestring
    """
    # TODO: complete with other methods
    if hasattr(obj, "get_documentation"):
        return obj.get_documentation()
    elif isinstance(obj, basestring):
        return obj
    elif hasattr(obj, "__doc__"):
        return obj.__doc__
    else:
        return str(obj)

